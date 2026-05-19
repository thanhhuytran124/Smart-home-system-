let config = {
    user: localStorage.getItem('aio_user') || "",
    key : localStorage.getItem('aio_key')  || ""
};

let mqttClient = null;

window.addEventListener('load', async function () {
    initGauges();
    updateClock();
    setInterval(updateClock, 1000);

    const token = localStorage.getItem('jwt_token');
    if (!token) {
        window.location.href = '/login.html';
        return;
    }
    try {
        const res = await fetch('/api/me', { headers: { 'Authorization': 'Bearer ' + token } });
        if (!res.ok) throw new Error('unauthorized');
        const me = await res.json();
        config.user = me.adafruit_user;
        config.key  = me.adafruit_key;
        localStorage.setItem('aio_user', me.adafruit_user);
        localStorage.setItem('aio_key',  me.adafruit_key);
        document.getElementById('info_username').textContent  = me.username;
        document.getElementById('info_aio_user').textContent  = me.adafruit_user;
        document.getElementById('info_aio_key').textContent   = me.adafruit_key.slice(0, 8) + "••••••••";
    } catch (e) {
        localStorage.clear();
        window.location.href = '/login.html';
        return;
    }

    if (config.user && config.key) {
        connectMQTT();
    } else {
        setMqttStatus('warn', 'Thiếu Adafruit key');
    }
});

function logout() {
    if (!confirm('Bạn có chắc muốn đăng xuất?')) return;
    localStorage.clear();
    window.location.href = '/login.html';
}

function updateClock() {
    const now = new Date();
    document.getElementById('digital-clock').innerText =
        now.toLocaleTimeString('vi-VN', { hour12: false }) + " | " + now.toLocaleDateString('vi-VN');
}

function connectMQTT() {
    if (!config.user || !config.key) return;

    setMqttStatus('connecting', 'Đang kết nối...');

    mqttClient = mqtt.connect('wss://io.adafruit.com/mqtt', {
        username       : config.user,
        password       : config.key,
        clientId       : 'yolohome_' + Math.random().toString(16).slice(3),
        reconnectPeriod: 5000,
        keepalive      : 60
    });

    mqttClient.on('connect', async () => {
        console.log('MQTT: Đã kết nối Adafruit IO');
        setMqttStatus('ok', 'Realtime');

        const feeds = ['temperature', 'humidity', 'light', 'fan-speed', 'led-rgb', 'door'];
        feeds.forEach(f => mqttClient.subscribe(`${config.user}/feeds/${f}`));

        await fetchInitialState(feeds);
    });

    mqttClient.on('message', (topic, message) => {
        const feed = topic.split('/feeds/')[1];
        handleFeedUpdate(feed, message.toString());
    });

    mqttClient.on('reconnect', () => {
        setMqttStatus('connecting', 'Kết nối lại...');
    });

    mqttClient.on('offline', () => {
        setMqttStatus('error', 'Mất kết nối');
    });

    mqttClient.on('error', err => {
        console.error('MQTT error:', err);
        setMqttStatus('error', 'Lỗi kết nối');
    });
}

async function fetchInitialState(feeds) {
    for (const f of feeds) {
        try {
            const res = await fetch(
                `https://io.adafruit.com/api/v2/${config.user}/feeds/${f}/data/last`,
                { headers: { 'X-AIO-Key': config.key } }
            );
            if (res.ok) {
                const data = await res.json();
                if (data && data.value !== undefined) handleFeedUpdate(f, data.value);
            }
        } catch (e) {}
    }
}

function handleFeedUpdate(feed, val) {
    if (feed === 'temperature') window.gaugeTemp.refresh(parseFloat(val));
    if (feed === 'humidity')    window.gaugeHumi.refresh(parseFloat(val));
    if (feed === 'light')       window.gaugeLight.refresh(parseFloat(val));
    if (feed === 'fan-speed')   updateFanUI(val);
    if (feed === 'led-rgb' && val && val.includes('#')) {
        updateRGBUI(val.includes(':') ? val.split(':')[1] : val);
    }
    if (feed === 'door') updateDoorUI(val);
}

function setMqttStatus(state, text) {
    const dot  = document.getElementById('mqtt-dot');
    const label = document.getElementById('mqtt-label');
    if (!dot || !label) return;
    const colors = { ok: '#27ae60', connecting: '#f39c12', warn: '#f39c12', error: '#e74c3c' };
    dot.style.background = colors[state] || '#ccc';
    label.textContent    = text;
}

async function postToAdafruit(feed, value) {
    if (!config.user || !config.key) {
        alert("Lỗi: Bạn chưa cấu hình User/Key trong tab Cài đặt!");
        return;
    }
    try {
        await fetch(`https://io.adafruit.com/api/v2/${config.user}/feeds/${feed}/data`, {
            method : 'POST',
            headers: { 'X-AIO-Key': config.key, 'Content-Type': 'application/json' },
            body   : JSON.stringify({ value: value })
        });
        console.log(`Đã gửi [${feed}]: ${value}`);
    } catch (e) {
        console.error("Lỗi gửi lệnh:", e);
    }
}

function updateFanLabel(val) { document.getElementById('fan-speed-text').innerText = val; }

async function sendFanSpeed(speed) {
    updateFanUI(speed);
    await postToAdafruit('fan-speed', speed);
}

function updateFanUI(speed) {
    const val    = parseInt(speed);
    const slider = document.getElementById('fan-slider');
    const text   = document.getElementById('fan-speed-text');
    if (slider) slider.value  = val;
    if (text)   text.innerText = val;

    const icon = document.getElementById('fan-icon');
    if (val > 0) {
        icon.classList.add('fan-on');
        icon.style.animationDuration = (2.1 - (val / 100 * 2)) + "s";
    } else {
        icon.classList.remove('fan-on');
    }
}

async function applyLEDColor() {
    const idx   = document.getElementById('led-index').value;
    const color = document.getElementById('rgb-picker').value;
    updateRGBUI(color);
    await postToAdafruit('led-rgb', `${idx}:${color}`);
}

async function sendLEDRaw(cmd) {
    if (cmd.startsWith('#')) updateRGBUI(cmd);
    await postToAdafruit('led-rgb', cmd);
}

function updateRGBUI(hex) {
    const icon = document.getElementById('rgb-icon');
    icon.style.color = (hex === '#000000' || hex === '0') ? '#ccc' : hex;
}

async function sendDoorCommand(cmd) {
    updateDoorUI(cmd);
    await postToAdafruit('door', cmd);
}

function updateDoorUI(val) {
    const icon  = document.getElementById('door-icon');
    const badge = document.getElementById('door-status-badge');
    if (!icon || !badge) return;

    const isOpen = (val === 'open' || val === '1');
    icon.className   = `fa-solid ${isOpen ? 'fa-door-open' : 'fa-door-closed'} device-icon`;
    icon.style.color = isOpen ? '#27ae60' : '#636e72';
    badge.textContent = isOpen ? 'ĐANG MỞ' : 'ĐÃ ĐÓNG';
    badge.className   = `door-badge ${isOpen ? 'door-open' : 'door-closed'}`;
}

function initGauges() {
    const cfg = { min: 0, max: 100, donut: true, pointer: false, gaugeWidthScale: 0.2, gaugeColor: '#f0f0f0', counter: true };
    window.gaugeTemp  = new JustGage({ id: 'gauge_temp',  value: 0, ...cfg, symbol: '°C', levelColors: ['#00BCD4', '#FFC107', '#F44336'] });
    window.gaugeHumi  = new JustGage({ id: 'gauge_humi',  value: 0, ...cfg, symbol: '%',  levelColors: ['#E1F5FE', '#42A5F5', '#01579B'] });
    window.gaugeLight = new JustGage({ id: 'gauge_light', value: 0, ...cfg, symbol: '%',  levelColors: ['#333',    '#FFD700', '#FFFF00'] });
}

function showSection(id, event) {
    document.querySelectorAll('.section').forEach(s => s.style.display = 'none');
    const target = document.getElementById(id);
    if (target) target.style.display = (id === 'settings') ? 'flex' : 'block';
    document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
    if (event) event.currentTarget.classList.add('active');
}

let relayList = [];
function openAddRelayDialog()  { document.getElementById('addRelayDialog').style.display = 'flex'; }
function closeAddRelayDialog() { document.getElementById('addRelayDialog').style.display = 'none'; }
function saveRelay() {
    const n = document.getElementById('relayName').value;
    const g = document.getElementById('relayGPIO').value;
    if (n && g) { relayList.push({ id: Date.now(), name: n, gpio: g, state: false }); renderRelays(); closeAddRelayDialog(); }
}
function renderRelays() {
    const c = document.getElementById('relayContainer'); c.innerHTML = '';
    relayList.forEach(r => {
        const d = document.createElement('div'); d.className = 'device-card';
        d.innerHTML = `<h3>${r.name}</h3><p>GPIO: ${r.gpio}</p><button class="toggle-btn ${r.state?'on':''}" onclick="toggleRelay(${r.id})">${r.state?'ON':'OFF'}</button>`;
        c.appendChild(d);
    });
}
async function toggleRelay(id) {
    const r = relayList.find(x => x.id === id);
    if (r) { r.state = !r.state; await postToAdafruit('relay', r.state ? 'ON' : 'OFF'); renderRelays(); }
}
