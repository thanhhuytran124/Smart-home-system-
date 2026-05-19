# KỊCH BẢN THUYẾT TRÌNH — YOLO HOME

> **Thời lượng dự kiến:** 12–14 phút thuyết trình + 3–5 phút Q&A
> **Đội ngũ:** Trần Thanh Huy · Nguyễn Phúc Nguyên · Trịnh Vũ Thiên Bảo · Đặng Trung Hiếu · Vũ Song Anh
> **Phân vai gợi ý (5 người):**
> - **Người 1 (Huy)** — Slides 1–4 + Slide 21 (mở đầu & kết thúc)
> - **Người 2 (Nguyên)** — Slides 5–7 (tổng quan hệ thống & phần cứng)
> - **Người 3 (Bảo)** — Slides 8–10 (cloud, feeds, deployment overview)
> - **Người 4 (Hiếu)** — Slides 11–14 (kiến trúc & firmware modules)
> - **Người 5 (Anh)** — Slides 15–20 (runtime, control, web, deployment, kết luận)

---

## SLIDE 1 — Tiêu đề & Giới thiệu đội (~30s)

**[Người 1 — Huy]**

> Xin chào thầy/cô và các bạn. Chúng em là Nhóm 1, gồm năm thành viên: Trần Thanh Huy, Nguyễn Phúc Nguyên, Trịnh Vũ Thiên Bảo, Đặng Trung Hiếu, và Vũ Song Anh.
>
> Hôm nay, nhóm em xin trình bày đề tài **"YOLO Home — Hệ thống nhà thông minh IoT"** — một dự án đa lĩnh vực kết hợp phần cứng nhúng, dịch vụ đám mây, dashboard trực quan trên web, cùng với một module mở rộng về nhận dạng khuôn mặt. Toàn bộ hệ thống được xây dựng trên nền tảng YoloBit ESP32, kết nối qua Adafruit IO.

---

## SLIDE 2 — Project Introduction (~45s)

**[Người 1 — Huy]**

> YOLO Home là một nền tảng giám sát và điều khiển nhà thông minh **gọn nhẹ nhưng thực tiễn**. Hệ thống kết nối các cảm biến và thiết bị chấp hành trên một board YoloBit ESP32 với dịch vụ Adafruit IO và một dashboard trên trình duyệt. Ngoài ra, chúng em còn phát triển một module nhận dạng khuôn mặt tuỳ chọn cho mục đích bảo mật.
>
> Bốn chức năng chính của hệ thống gồm:
> - **Một**, giám sát môi trường thời gian thực — nhiệt độ, độ ẩm, ánh sáng.
> - **Hai**, hiển thị song song trên LCD vật lý và dashboard cloud.
> - **Ba**, điều khiển từ xa quạt mini, LED RGB, và prototype relay.
> - **Bốn**, tích hợp nhận dạng khuôn mặt bằng OpenCV.

---

## SLIDE 3 — Why it matters (~50s)

**[Người 1 — Huy]**

> Vậy tại sao đề tài này lại có ý nghĩa?
>
> Thứ nhất, **xu hướng** — nhà thông minh và edge computing đang phát triển nhanh, kéo theo nhu cầu về các hệ thống kết nối, dễ triển khai, và dễ mở rộng.
>
> Thứ hai, **nhu cầu người dùng** — họ cần một hệ thống vừa đo đạc tin cậy, vừa điều khiển từ xa được, giao diện thân thiện, và có thể thêm các tính năng bảo mật như nhận dạng khuôn mặt hay điều khiển cửa.
>
> Thứ ba, **cách tiếp cận của nhóm** — chúng em kết hợp **MicroPython trên ESP32** để xử lý phần thiết bị, **Adafruit IO feeds** làm cầu nối cloud, **dashboard web** cho giao diện người dùng, và một **module Computer Vision riêng biệt** cho nhận dạng khuôn mặt. Mỗi tầng giải quyết một vai trò rõ ràng.

---

## SLIDE 4 — Project Objectives (~40s)

**[Người 1 — Huy]**

> Năm mục tiêu cụ thể của dự án:
>
> 1. **Thu thập** dữ liệu môi trường từ cảm biến và publish lên Adafruit IO.
> 2. **Hiển thị** giá trị thời gian thực trên dashboard web và LCD1602 tại chỗ.
> 3. **Điều khiển từ xa** quạt và đèn LED NeoPixel thông qua cloud.
> 4. **Modular hoá firmware** — chia tách module rõ ràng để dễ bảo trì và mở rộng.
> 5. **Hỗ trợ nhận dạng khuôn mặt** như một module có thể gắn vào.
>
> Bây giờ, em xin mời bạn Nguyên trình bày kiến trúc tổng thể.

---

## SLIDE 5 — System Overview (~60s)

**[Người 2 — Nguyên]**

> Cảm ơn bạn Huy. Hệ thống YOLO Home gồm **ba khối lớn** kết nối qua một cloud trung tâm.
>
> **Khối thứ nhất — YoloBit ESP32.** Đây là bộ não phần cứng, viết bằng MicroPython, có nhiệm vụ đọc cảm biến, chạy logic điều khiển, và publish hoặc subscribe các topic qua MQTT.
>
> **Khối thứ hai — Web Dashboard.** Là giao diện trên trình duyệt, dùng Adafruit IO REST API để lấy dữ liệu, và thư viện JustGage để vẽ các đồng hồ đo trực quan.
>
> **Khối thứ ba — Face Recognizer.** Một module standalone chạy trên PC, dùng Python + OpenCV + thuật toán LBPH để nhận dạng khuôn mặt cục bộ.
>
> **Adafruit IO** đóng vai trò là cloud hub kết nối thiết bị và dashboard — telemetry đi qua feeds, command cũng đi qua feeds.

---

## SLIDE 6 — Kiến trúc 3 tầng (~60s)

**[Người 2 — Nguyên]**

> Khi nhìn theo mô hình kinh điển, hệ thống được tách thành **3 tầng** rõ ràng để dễ scale và bảo trì.
>
> **Tầng ứng dụng (Application Layer)** — chứa Web Dashboard và Face Recognizer. Đây là nơi tương tác trực tiếp với người dùng.
>
> **Tầng cloud (Cloud Layer)** — Adafruit IO, vận hành MQTT broker, REST API, và lưu trữ các feed.
>
> **Tầng thiết bị (Device Layer)** — YoloBit ESP32 với các cảm biến và actuator.
>
> Ở tầng truyền tải, chúng em dùng **MQTT** cho messaging real-time giữa thiết bị và cloud, còn **REST API** cho phía dashboard polling giá trị mới nhất. Mỗi giao thức tận dụng đúng thế mạnh của nó.

---

## SLIDE 7 — Hardware Components (~60s)

**[Người 2 — Nguyên]**

> Về phần cứng cụ thể, chúng em sử dụng 7 thiết bị:
>
> - **YoloBit ESP32** — bộ điều khiển chính, dual-core 32-bit, Wi-Fi 2.4 GHz tích hợp, chạy MicroPython.
> - **DHT20** — cảm biến nhiệt độ và độ ẩm số, giao tiếp I²C, độ chính xác ±0.5 °C và ±3% RH.
> - **Quang trở (Light Sensor)** — đọc tín hiệu analog ở chân pin2, quy đổi sang phần trăm cường độ sáng.
> - **LCD1602** — màn hình 16×2 ký tự, giao tiếp I²C, hiển thị thông số tại chỗ kèm đồng hồ.
> - **Quạt mini DC** — điều khiển tốc độ qua PWM tại chân pin10.
> - **Chuỗi 4 LED NeoPixel WS2812B** — LED RGB địa chỉ riêng từng pixel, tín hiệu 1 dây tại pin0.
> - **Module relay** — prototype để điều khiển thiết bị điện 220V.
>
> Em xin mời bạn Bảo nói về phần cloud.

---

## SLIDE 8 — Cloud Platform: Adafruit IO (~60s)

**[Người 3 — Bảo]**

> Cảm ơn Nguyên. Về nền tảng cloud, nhóm chọn **Adafruit IO** vì ba lý do.
>
> Thứ nhất, nó cung cấp một **MQTT broker** trên port 1883 — phù hợp với thiết bị embedded vì lightweight, latency thấp, và hỗ trợ pub/sub.
>
> Thứ hai, nó có **REST API v2** trên HTTPS — rất tiện cho phía dashboard browser, chỉ cần fetch với header `X-AIO-Key` là đọc được giá trị mới nhất.
>
> Thứ ba, **mô hình feed** — mỗi loại dữ liệu hoặc lệnh được map vào một channel rời, có lưu lịch sử time-series, có authentication bằng AIO Key.
>
> Trong dự án, chúng em **kết hợp cả hai giao thức**: thiết bị dùng MQTT để thông tin push tới ngay lập tức, còn dashboard dùng REST polling mỗi 5 giây để cập nhật gauge.

---

## SLIDE 9 — Feeds & Data Flow (~75s)

**[Người 3 — Bảo]**

> Hệ thống định nghĩa **6 feed**, mỗi feed có vai trò riêng:
>
> - `temperature`, `humidity`, `light` — uplink, từ YoloBit lên cloud, lưu giá trị cảm biến.
> - `fan-speed` — feed hai chiều, vừa nhận lệnh từ web vừa phản hồi trạng thái lên cloud.
> - `led-rgb` — downlink, từ web xuống thiết bị, mang chuỗi màu hex.
> - `relay` — downlink, prototype điều khiển relay.
>
> **Feed chính là single source of truth** cho cả telemetry lẫn command state. Bất kỳ client nào subscribe cũng nhận được cùng giá trị.
>
> Về cadence: uplink — cảm biến publish **mỗi 5 giây một lần**. Downlink — dashboard POST tới feed, Adafruit IO chuyển tiếp qua MQTT đến thiết bị đang subscribe — độ trễ cảm nhận được là dưới 1 giây.

---

## SLIDE 10 — Firmware, Control & Future Work (Overview) (~70s)

**[Người 3 — Bảo]**

> Slide này tổng kết toàn bộ phần firmware và hướng phát triển. Em sẽ điểm qua bốn ý chính, bạn Hiếu sẽ đi sâu vào từng module ở các slide kế tiếp.
>
> **Một** — Firmware modular: 7 file Python, mỗi file một trách nhiệm — config, network, mqtt, coreiot, fan, rgb, và main loop.
>
> **Hai** — Control: quạt dùng PWM trên pin10 với công thức `duty = speed × 10.23`, được clamp trong khoảng 0 đến 1023. LED RGB nhận chuỗi `#RRGGBB`, được hàm `hex_to_rgb()` chuyển thành tuple để ghi xuống NeoPixel.
>
> **Ba** — Deployment: dùng **Pymakr trong VS Code** để upload file MicroPython. Board tự động chạy `main.py` sau khi reset, kết nối Wi-Fi rồi vào loop.
>
> **Bốn** — Face Recognition standalone: pipeline gồm Haar Cascade phát hiện khuôn mặt → LBPH huấn luyện trên ảnh có nhãn → model serialized → nhận dạng real-time từ webcam.
>
> Em mời Hiếu trình bày chi tiết kiến trúc và module.

---

## SLIDE 11 — Architecture & Control Flow (Section Intro) (~30s)

**[Người 4 — Hiếu]**

> Cảm ơn Bảo. Phần tiếp theo em sẽ đi sâu vào kỹ thuật — chúng ta sẽ xem cụ thể luồng dữ liệu uplink và downlink, cấu trúc các module firmware, hành vi của main loop, logic điều khiển từng actuator, tích hợp web dashboard, và cuối cùng là quy trình deployment.

---

## SLIDE 12 — Uplink Data Flow (~70s)

**[Người 4 — Hiếu]**

> Bắt đầu với **luồng uplink** — từ cảm biến lên dashboard. Chu trình này lặp lại mỗi 5 giây.
>
> **Bước 1**: `main.py` đọc cảm biến DHT20 lấy nhiệt độ, độ ẩm; đọc chân analog pin2 lấy ánh sáng.
> **Bước 2**: `coreiot_module` format các giá trị, gọi `mqtt.publish()` lên broker.
> **Bước 3**: Adafruit IO nhận và lưu vào feed tương ứng.
> **Bước 4**: Dashboard, sau khi đã login với AIO Key, gọi REST API endpoint `/data/last` của từng feed.
> **Bước 5**: Mỗi giá trị được đưa vào `JustGage.refresh()` để các đồng hồ đo cập nhật mượt mà.
>
> Toàn bộ pipeline bất đồng bộ — thiết bị không cần biết dashboard có online hay không, và ngược lại.

---

## SLIDE 13 — Downlink Control Flow (~70s)

**[Người 4 — Hiếu]**

> Ngược lại là **luồng downlink** — từ thao tác người dùng xuống thiết bị, độ trễ thấp.
>
> **Bước 1**: Người dùng kéo slider quạt hoặc chọn màu RGB trên dashboard.
> **Bước 2**: `script.js` gửi HTTP POST đến Adafruit IO REST API.
> **Bước 3**: Adafruit IO tiếp nhận và push tin nhắn qua MQTT.
> **Bước 4**: Trên YoloBit, `mqtt.check_msg()` trong main loop bắt được message và dispatch tới callback đã đăng ký.
> **Bước 5**: Callback cập nhật trực tiếp PWM cho quạt hoặc trạng thái NeoPixel cho LED.
>
> Một lưu ý thiết kế quan trọng: tất cả các callback đều **lightweight và non-blocking** — không có vòng lặp hay sleep dài bên trong — để giữ độ phản hồi real-time.

---

## SLIDE 14 — Firmware Module Design (~80s)

**[Người 4 — Hiếu]**

> Đây là sơ đồ phụ thuộc các module firmware. Mỗi file đảm nhận một vai trò rõ rệt:
>
> - **`config.py`** — chỉ chứa credentials Wi-Fi, AIO Key, và tên feed. Không có logic.
> - **`network_module.py`** — kết nối Wi-Fi, đồng bộ NTP, xử lý reconnect.
> - **`mqtt.py`** — class bao bọc `umqtt.simple`, quản lý publish/subscribe và keepalive. Triển khai theo singleton.
> - **`coreiot_module.py`** — facade giữa MQTT và feed Adafruit IO, có cơ chế auto-reconnect khi publish lỗi.
> - **`fan_module.py`** và **`rgb_module.py`** — driver actuator: một cho PWM, một cho NeoPixel.
> - **`main.py`** — orchestrator, gọi tất cả module trên trong vòng lặp chính.
>
> Cách phân chia này tuân theo **nguyên tắc đơn trách nhiệm (SRP)** — mỗi module có thể được test độc lập, và việc thêm tính năng mới như relay hay sensor mới chỉ cần thêm một module riêng.
>
> Em xin mời bạn Song Anh trình bày phần runtime và control logic.

---

## SLIDE 15 — Main Loop Operation (~70s)

**[Người 5 — Anh]**

> Cảm ơn Hiếu. Bây giờ em đi vào **main loop** — vòng lặp chính của firmware. Chúng em ưu tiên 4 việc, theo thứ tự:
>
> **Một** — Poll MQTT: ngay đầu mỗi vòng, gọi `check_msg()` để nhận lệnh điều khiển sớm nhất có thể.
> **Hai** — Đọc cảm biến: DHT20 cho nhiệt-ẩm, ADC cho ánh sáng. Có validate giá trị trước khi sử dụng.
> **Ba** — Hiển thị và publish: cập nhật LCD ngay (rất mượt), nhưng publish lên cloud chỉ mỗi 5 giây — tách rời 2 tốc độ để không lãng phí bandwidth.
> **Bốn** — Error handling: toàn bộ vòng được bọc `try/except`. Nếu I²C glitch hay mất Wi-Fi tạm thời, chỉ log ra serial rồi tiếp tục vòng, không bao giờ crash.
>
> **Timing**: `sleep(0.1)` giữa các vòng — đủ ngắn để latency điều khiển dưới 100 ms, đủ dài để không ngốn CPU.

---

## SLIDE 16 — Fan Control: PWM Mapping & Safety (~50s)

**[Người 5 — Anh]**

> Đi vào chi tiết điều khiển quạt — phần hardware là quạt DC nhỏ nối với pin10 qua transistor driver, software điều khiển bằng PWM.
>
> **Công thức ánh xạ**: `PWM duty = fan_speed_percent × 10.23`.
>
> Hằng số 10.23 đến từ độ phân giải PWM 10-bit của ESP32 — giá trị tối đa là 1023. Khi user đưa vào 100%, công thức cho 1023. Khi 75%, ta được 767. Khi 0%, đương nhiên là 0.
>
> **Validation**: input được clamp về khoảng [0, 100] trước khi nhân — để tránh PWM tràn và bảo vệ phần cứng. Đây là chi tiết nhỏ nhưng quan trọng khi nhận dữ liệu từ cloud — không bao giờ tin tưởng tuyệt đối vào giá trị bên ngoài.

---

## SLIDE 17 — RGB LED Control: NeoPixel Command Model (~50s)

**[Người 5 — Anh]**

> Với LED RGB, command model rất đơn giản — chấp nhận 3 dạng input:
>
> **Một**: chuỗi hex `#RRGGBB`. Ví dụ `#00FF00` được hàm `hex_to_rgb()` chuyển thành tuple `(0, 255, 0)` — màu xanh lá thuần.
>
> **Hai**: chuỗi `"0"` hoặc `"#000000"` — tắt toàn bộ 4 LED.
>
> **Ba**: keyword đặc biệt `"ALARM"` — reserve cho chế độ báo động sau này, ví dụ nháy đỏ pulse.
>
> Vòng `for` ghi cùng một màu cho cả 4 pixel rồi gọi `pixels.write()` để flush. Lưu ý thực tế: chúng em đang cân nhắc thêm **rate limiting** cho các lệnh đổi màu liên tiếp — vì nếu user kéo color picker quá nhanh sẽ gây spike CPU không cần thiết.

---

## SLIDE 18 — Web Dashboard: Architecture & Features (~60s)

**[Người 5 — Anh]**

> Về dashboard, **frontend stack** gồm: HTML thuần, CSS thuần, JavaScript ES6+, thư viện JustGage cho gauge, và Font Awesome cho icon. Backend duy nhất là Adafruit IO REST + MQTT, không có server riêng.
>
> Hai cụm tính năng chính:
>
> **Cụm thứ nhất — Gauges**: ba đồng hồ đo cho nhiệt độ, độ ẩm, ánh sáng, mỗi cái có gradient màu riêng và refresh mỗi 5 giây.
>
> **Cụm thứ hai — Controls**: slider điều khiển quạt với animation icon xoay theo tốc độ; color picker cho LED RGB. Credentials Adafruit IO được lưu vào `localStorage` để user chỉ phải nhập một lần.
>
> Ưu điểm thiết kế "static-only": user chỉ cần mở file `index.html` là chạy, không cần dựng server.

---

## SLIDE 19 — Deployment Workflow với Pymakr (~70s)

**[Người 5 — Anh]**

> Phần triển khai firmware — chúng em dùng **Pymakr extension** trong VS Code. Quy trình 5 bước:
>
> **Bước 1**: Mở thư mục `esp32/` làm workspace trong VS Code.
> **Bước 2**: Sửa file `config.py` — điền SSID, password Wi-Fi, AIO Username, AIO Key.
> **Bước 3**: Cắm board qua USB, Pymakr tự nhận serial port.
> **Bước 4**: Bấm **Upload** — Pymakr push toàn bộ file qua serial REPL ở tốc độ 115200 baud.
> **Bước 5**: Pymakr tự issue soft reset; board boot, chạy `main.py`, kết nối Wi-Fi và Adafruit IO, bắt đầu publish.
>
> Lời khuyên thực tế: luôn để **serial monitor mở** trong lần boot đầu — để xác nhận kết nối Wi-Fi và MQTT thành công, đồng thời thấy ngay nếu có exception runtime. Pymakr tích hợp REPL trực tiếp trong VS Code nên việc debug rất gọn.

---

## SLIDE 20 — Conclusion & Future Development (~65s)

**[Người 5 — Anh]**

> Tổng kết — nhóm em đã giao được:
>
> - **Giám sát môi trường** thời gian thực với 3 cảm biến.
> - **Kết nối cloud** đầy đủ với Adafruit IO.
> - **Điều khiển từ xa** quạt và LED RGB.
> - **Dashboard trực quan** trên trình duyệt.
> - **Module Face Recognition** standalone hoạt động được trên video test.
>
> Hướng phát triển tiếp theo gồm 4 nhánh:
>
> 1. Hoàn thiện firmware relay để điều khiển thiết bị 220 V thực tế.
> 2. Thêm chế độ **RGB alarm** với pulse và pattern.
> 3. **Mobile app** và quản lý user có xác thực.
> 4. **Lưu lịch sử telemetry** để phân tích xu hướng.
>
> Về mặt kỹ thuật, chúng em dự định: harden callbacks MQTT, rate-limit lệnh UI, thêm persistent state khi reconnect, và đặc biệt là **OTA update** cho firmware để không phải cắm USB mỗi lần cập nhật.

---

## SLIDE 21 — Thank You & Q&A (~20s)

**[Người 1 — Huy quay lại đóng]**

> Bài thuyết trình của Nhóm 1 đến đây là hết. Chúng em xin cảm ơn thầy/cô và các bạn đã lắng nghe. Bây giờ, nhóm rất sẵn sàng nhận câu hỏi và đóng góp ý kiến từ mọi người. Xin mời ạ.

---

## PHỤ LỤC: Các câu hỏi Q&A dự kiến

Dưới đây là một số câu có khả năng được hỏi, kèm gợi ý trả lời:

### Q1: Tại sao chọn Adafruit IO mà không phải MQTT broker tự host?
> Vì Adafruit IO miễn phí ở mức giáo dục, có sẵn cả MQTT broker và REST API, hỗ trợ auth bằng AIO Key đơn giản. Tự host (ví dụ Mosquitto + InfluxDB + Grafana) mạnh hơn nhưng tốn công deploy. Sau này nếu cần scale, chúng em sẽ chuyển sang stack tự host.

### Q2: LBPH có chính xác không? Sao không dùng FaceNet hay ArcFace?
> LBPH có chính xác kém hơn các mô hình deep learning. Nhóm chọn LBPH vì nó chạy được trên CPU, không cần GPU, train được chỉ với vài chục ảnh — phù hợp scope giáo dục. Nâng cấp lên FaceNet là một hướng phát triển tiếp theo.

### Q3: Polling mỗi 5 giây có gây tải Adafruit IO không?
> Adafruit IO free tier giới hạn 30 publish/phút. Với 4 feed × 12 lần/phút = 48 — vẫn trong giới hạn. Nếu vượt, ta có thể chuyển dashboard sang dùng MQTT WebSocket thay vì REST polling.

### Q4: Nếu mất Wi-Fi giữa chừng thì sao?
> Hàm `publish_sensor_data()` có cơ chế **auto-reconnect**: nếu publish thất bại, nó gọi lại `connect_ww_or_tt()` ngay. Toàn bộ main loop được bọc `try/except` nên một lỗi mạng tạm thời chỉ in log và tiếp tục — không crash.

### Q5: Tại sao công thức là `× 10.23` mà không phải `× 10.24`?
> Vì PWM 10-bit có giá trị từ 0 đến **1023** (không phải 1024). Khi `speed = 100`, ta cần duty `= 1023`. `100 × 10.23 = 1023`. Dùng 10.24 sẽ ra 1024 — vượt giới hạn.

### Q6: Có thể thêm sensor mới như nào?
> Nhờ kiến trúc modular: chỉ cần (1) viết driver sensor mới trong file riêng, (2) thêm dòng đọc trong `main.py`, (3) thêm feed trong `config.py`, (4) thêm `mqtt.publish()` trong `coreiot_module.py`. Web dashboard chỉ cần thêm một gauge.

### Q7: Bảo mật cho hệ thống thế nào?
> Hiện tại: AIO Key kiểm soát truy cập cloud, Wi-Fi WPA2 bảo vệ tầng mạng. Hướng phát triển: thêm JWT auth ở backend (slide tương lai), HTTPS cho MQTT (port 8883), và OTA update có chữ ký.

---

## CHECKLIST CHUẨN BỊ TRƯỚC KHI THUYẾT TRÌNH

- [ ] Kiểm tra demo thiết bị YoloBit hoạt động và kết nối Wi-Fi ổn định.
- [ ] Mở sẵn dashboard với credentials thật để biểu diễn (nếu được demo trực tiếp).
- [ ] Chuẩn bị video backup demo nếu mạng không ổn định.
- [ ] Test slide trên máy chiếu — kiểm tra font hiển thị tiếng Việt và emoji.
- [ ] In ra hoặc mở SCRIPT.md trên tablet/điện thoại để tham khảo.
- [ ] Đồng bộ thứ tự phát biểu giữa 5 thành viên — tập một lần đầy đủ.
- [ ] Phân công người bấm slide tiếp theo (nếu không tự bấm).
- [ ] Chuẩn bị câu mở đầu tự nhiên và lời cảm ơn cuối.
- [ ] Tổng thời lượng: nhắm tới **12–14 phút thuyết trình + 3–5 phút Q&A**.
