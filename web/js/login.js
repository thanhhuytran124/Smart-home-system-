const API = "/api";

function showLogin() {
    document.getElementById('loginForm').style.display    = 'block';
    document.getElementById('registerForm').style.display = 'none';
    clearMessage();
}

function showRegister() {
    document.getElementById('loginForm').style.display    = 'none';
    document.getElementById('registerForm').style.display = 'block';
    clearMessage();
}

function showMessage(text, type = 'error') {
    const el = document.getElementById('auth-message');
    el.textContent = text;
    el.className   = 'auth-message ' + type;
}

function clearMessage() {
    showMessage('', '');
}

if (localStorage.getItem('jwt_token')) {
    window.location.href = '/index.html';
}

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('login_user').value.trim();
    const password = document.getElementById('login_pass').value;

    try {
        const res = await fetch(`${API}/login`, {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify({ username, password })
        });
        const data = await res.json();

        if (!res.ok) {
            showMessage(data.detail || 'Đăng nhập thất bại');
            return;
        }

        localStorage.setItem('jwt_token',  data.token);
        localStorage.setItem('username',   data.username);
        localStorage.setItem('aio_user',   data.adafruit_user);
        localStorage.setItem('aio_key',    data.adafruit_key);

        showMessage('Đăng nhập thành công! Đang chuyển hướng...', 'success');
        setTimeout(() => window.location.href = '/index.html', 600);
    } catch (err) {
        showMessage('Lỗi kết nối tới backend');
    }
});

document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const body = {
        username:      document.getElementById('reg_user').value.trim(),
        password:      document.getElementById('reg_pass').value,
        adafruit_user: document.getElementById('reg_aio_user').value.trim(),
        adafruit_key:  document.getElementById('reg_aio_key').value.trim(),
    };

    try {
        const res = await fetch(`${API}/register`, {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify(body)
        });
        const data = await res.json();

        if (!res.ok) {
            showMessage(data.detail || 'Đăng ký thất bại');
            return;
        }

        const registeredUsername = body.username;
        showMessage('Đăng ký thành công! Vui lòng đăng nhập.', 'success');

        document.getElementById('registerForm').reset();

        setTimeout(() => {
            showLogin();
            document.getElementById('login_user').value = registeredUsername;
            document.getElementById('login_pass').focus();
        }, 800);
    } catch (err) {
        console.error('Register error:', err);
        showMessage('Lỗi kết nối tới backend: ' + err.message);
    }
});
