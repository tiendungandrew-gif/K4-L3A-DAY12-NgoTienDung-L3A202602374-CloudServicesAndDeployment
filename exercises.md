# Phiếu Phản Ánh — K4 Level 3A, Ngày 12

> **Bài làm cá nhân.** Trả lời bằng lời của chính bạn, dựa trên những gì bạn
> quan sát được khi chạy code — không sao chép đáp án của người khác.
>
> Cách trả lời: điền câu trả lời chi tiết cho từng câu hỏi bên dưới.
> `grade.py` đếm số câu đã trả lời (15 điểm cho 10 câu).
>
> Họ và tên: Ngô Tiến Dũng  Mã học viên: L3A202602374

---

### Câu 1 — Fail fast (CP1)

Trong `Settings`, `agent_api_key` không có giá trị mặc định nên app chết ngay
khi khởi động nếu thiếu biến môi trường. Hãy mô tả một tình huống cụ thể mà
việc "chết sớm" này cứu bạn, so với việc để mặc định `"changeme"`.

Nếu ta đặt giá trị mặc định là `"changeme"`, khi deploy lên Cloud hoặc đưa vào môi trường Production mà lập trình viên/DevOps vô tình quên cấu hình biến môi trường `AGENT_API_KEY` (hoặc file cấu hình bị thiếu/sai tên biến), container vẫn sẽ khởi động bình thường và báo trạng thái Healthy. Khi đó:
1. Hệ thống mở cửa API ra Internet với khóa bảo vệ mặc định là `"changeme"`. Bất kỳ ai hay con bot scan tự động nào cũng có thể gửi request với header `X-API-Key: changeme` để gọi API, bòn rút token LLM, gây cạn kiệt ngân sách hoặc đánh cắp dữ liệu trò chuyện của người dùng.
2. Với cơ chế **Fail-fast** (không có giá trị mặc định): Ứng dụng sẽ ném ngoại lệ `ValidationError` từ Pydantic và dừng ngay lập tức lúc khởi động (`startup`). Lỗi này lập tức kích hoạt cảnh báo trên Dashboard của Cloud Platform (Render/Railway báo Crash/Failed deploy), ngăn chặn việc traffic công khai trỏ vào một service không an toàn và buộc lập trình viên phải cấu hình khóa bí mật hợp lệ ngay trước khi phục vụ người dùng.

---

### Câu 2 — Log cho máy đọc (CP1)

Chạy service và gọi `/ask` vài lần. Dán một dòng log JSON bạn thu được, rồi
nêu **hai** việc bạn làm được với dòng log đó mà `print("đã trả lời xong")`
không làm được.

- Dòng log JSON thu được trong thực tế:
```json
{"event": "ask_completed", "level": "info", "timestamp": "2026-09-28T09:29:23.754812Z", "user_id": "anonymous", "tokens_in": 1, "tokens_out": 35, "cost_usd": 2.115e-05}
```
- Hai việc làm được với dòng log JSON này mà `print("đã trả lời xong")` không làm được:
1. **Phân tích số liệu và giám sát chi phí tự động (Aggregation & Metric Alerting):** Các công cụ phân tích log tập trung (như Datadog, ELK Stack, Grafana Loki, CloudWatch) có thể parse trực tiếp các trường số `tokens_in`, `tokens_out`, `cost_usd` để vẽ dashboard theo dõi chi phí LLM theo thời gian thực, hoặc tự động kích hoạt cảnh báo (Alert) nếu `cost_usd` của một request vượt ngưỡng bất thường. Ngược lại, `print()` dạng plain text đòi hỏi phải viết Regex phức tạp và dễ gãy khi định dạng thay đổi.
2. **Truy vấn, lọc và gỡ lỗi theo định danh người dùng (Structured Querying & Filtering):** Khi có sự cố hoặc tranh chấp về cước phí, ta có thể chạy query JSON chính xác như `event = "ask_completed" AND user_id = "user_123"` để trích xuất toàn bộ lịch sử sử dụng và lượng token của người dùng đó trong vài mili-giây. Câu lệnh `print("đã trả lời xong")` không có metadata định danh (ai gọi, tốn bao nhiêu token, thời gian ISO chính xác nào) nên hoàn toàn vô dụng trong việc đối soát dữ liệu production.

---

### Câu 3 — Kích thước image (CP2)

Build cả hai phiên bản và ghi lại số đo thật:

```bash
docker build -f <Dockerfile-1-stage> -t agent:single .
docker build -t agent:multi .
docker images | grep agent
```

| Bản | Dung lượng |
|-----|-----------|
| 1 stage (bản đầu) | ~320 MB |
| Multi-stage | ~145 MB |

Giải thích: phần dung lượng chênh lệch đó là những gì?

Phần dung lượng chênh lệch (giảm hơn 50%) bao gồm:
1. **Công cụ build và cache của pip:** Trong stage `builder`, quá trình chạy `pip install` sinh ra cache tải về (`~/.cache/pip`), các file tạm unpack thư viện bánh xe (wheel) và các file build trung gian. Khi chuyển sang stage `runtime`, chúng ta chỉ sao chép kết quả đã cài đặt ở thư mục `/install` sang một image python-slim sạch, loại bỏ hoàn toàn các cache và công cụ thừa này.
2. **Loại bỏ file rác nhờ `.dockerignore`:** Không sao chép các file môi trường ảo `.venv`, thư mục git `.git`, bộ nhớ đệm `__pycache__`, và các tài liệu test vào image production.
3. **Giảm số lượng layer lịch sử:** Trong multi-stage, các lệnh thao tác cài đặt nặng nề ở builder không bị ghi lại vào metadata và filesystem layer của image cuối cùng.

---

### Câu 4 — Thứ tự lệnh trong Dockerfile (CP2)

Sửa một ký tự trong `app/main.py` rồi build lại. Với Dockerfile của bạn, những
layer nào được dùng lại từ cache, layer nào phải chạy lại? Nếu bạn đặt
`COPY . .` lên trước `RUN pip install` thì kết quả khác thế nào?

- **Với Dockerfile hiện tại (tối ưu):**
  - Các layer từ đầu cho tới trước `COPY app/ ./app` (gồm: base image, `WORKDIR`, cài đặt package trong stage builder, tạo `appuser`, `COPY --from=builder /install`) đều được **DÙNG LẠI TỪ CACHE (CACHED)**.
  - Chỉ có layer `COPY app/ ./app` và các chỉ thị phía sau (`USER`, `EXPOSE`, `CMD`) mới phải chạy lại. Quá trình rebuild diễn ra cực nhanh (dưới 1 giây).
- **Nếu đặt `COPY . .` lên trước `RUN pip install`:**
  - Bất cứ khi nào sửa dù chỉ một ký tự trong code (`app/main.py`), layer `COPY . .` sẽ bị đổi hash checksum $\rightarrow$ làm **vô hiệu hóa (invalidate) toàn bộ cache** từ bước đó trở đi.
  - Docker sẽ bị ép buộc phải chạy lại toàn bộ lệnh `RUN pip install` từ đầu ở mỗi lần build, tải lại toàn bộ các thư viện qua mạng, khiến thời gian build tăng vọt từ 1 giây lên hàng chục giây đến vài phút và gây nghẽn băng thông của pipeline CI/CD.

---

### Câu 5 — Vì sao không chạy bằng root (CP2)

Container mặc định chạy bằng root. Mô tả chuỗi sự kiện dẫn từ "một lỗ hổng
trong code Python của bạn" tới "kẻ tấn công có quyền cao trên máy host", và
lệnh `USER` cắt đứt chuỗi đó ở chỗ nào.

- **Chuỗi sự kiện (Container Escape & Privilege Escalation):**
  1. *Bước 1 (Khai thác ứng dụng):* Ứng dụng Python chứa lỗ hổng thực thi mã từ xa (RCE - ví dụ qua `eval()`, lỗ hổng thư viện hoặc command injection).
  2. *Bước 2 (Chiếm quyền root container):* Kẻ tấn công gửi payload kích hoạt RCE và mở được một shell điều khiển trong container. Do container mặc định không khai báo `USER`, tiến trình Python chạy dưới quyền **root (UID 0)** trong container namespace.
  3. *Bước 3 (Thoát container ra máy host):* Vì sở hữu UID 0, nếu container không bị giới hạn nghiêm ngặt hoặc máy host có lỗ hổng Linux Kernel (như Dirty COW), hoặc container có mount các volume nhạy cảm (như `/var/run/docker.sock`), kẻ tấn công có thể tương tác trực tiếp với kernel/daemon của host, sửa đổi file hệ điều hành host và chiếm toàn quyền kiểm soát (root) toàn bộ máy chủ vật lý.
- **Lệnh `USER appuser` cắt đứt chuỗi ở đâu:**
  - Chỉ thị `USER appuser` chuyển tiến trình sang chạy với người dùng thường (UID 10001, không có quyền sudo). Khi kẻ tấn công khai thác RCE ở Bước 1, chúng bị giam trong phạm vi quyền hạn tối thiểu của `appuser`: không thể ghi vào thư mục hệ thống của container, không có Linux Capabilities nhạy cảm, và không thể thao tác với docker socket để thực hiện container escape ở Bước 2 và Bước 3.

---

### Câu 6 — Cửa sổ trượt (CP3)

Rate limit của bạn dùng sliding window 60 giây. Nếu thay bằng cách đếm theo
phút đồng hồ (reset lúc giây 00), một người dùng có thể gửi tối đa bao nhiêu
request trong 2 giây liên tiếp khi hạn mức là 10/phút? Giải thích cách đạt được
con số đó.

- Một người dùng có thể gửi tối đa **20 request** trong 2 giây liên tiếp.
- **Giải thích cách đạt được (Lỗ hổng ranh giới - Fixed Window Boundary Burst):**
  - Cơ chế đếm theo phút đồng hồ chia thời gian thành các khung cố định (ví dụ từ `12:00:00` đến `12:00:59`, và reset bộ đếm về 0 lúc `12:01:00`).
  - Kẻ tấn công đợi đến giây cuối cùng của khung giờ thứ nhất (`12:00:59`) và gửi dồn dập **10 request** (vừa đủ hạn mức cho phép của phút 12:00).
  - Ngay 1 giây sau, khi đồng hồ điểm `12:01:00`, bộ đếm được reset về 0. Kẻ tấn công lập tức bắn tiếp **10 request** nữa.
  - Kết quả: Chỉ trong 2 giây liên tiếp (`12:00:59` và `12:01:00`), hệ thống đã phải tiếp nhận $10 + 10 = 20$ request (tăng đột biến gấp đôi tải quy định).
  - Thuật toán **Sliding Window** (sử dụng Redis Sorted Set) khắc phục triệt để lỗi này bằng cách luôn tính toán tổng số request trong đúng 60 giây trượt lùi tính từ thời điểm hiện tại `[now - 60, now]`.

---

### Câu 7 — Rate limit và cost guard (CP3)

Hai cơ chế này khác nhau ở điểm nào? Cho một tình huống mà rate limit cho qua
nhưng cost guard phải chặn, và một tình huống ngược lại.

- **Khác biệt cốt lõi:**
  - *Rate Limit:* Giám sát **tần suất thao tác (vận tốc request)** trong một khung thời gian ngắn (ví dụ: tối đa 10 request/phút) để bảo vệ hạ tầng máy chủ khỏi nguy cơ quá tải tài nguyên mạng, CPU và tấn công từ chối dịch vụ (DoS/Spam).
  - *Cost Guard:* Giám sát **tổng ngân sách chi tiêu tích lũy (tài chính)** trong chu kỳ dài hạn (ví dụ: tối đa 10.0 USD/tháng) dựa trên tổng số token LLM tiêu thụ thực tế để bảo vệ ví tiền và ngân sách vận hành của doanh nghiệp.
- **Tình huống Rate Limit cho qua nhưng Cost Guard chặn:**
  - Người dùng gửi 1 request duy nhất trong cả tiếng đồng hồ (tốc độ cực thấp, 1 req/h $\ll$ 10 req/phút $\rightarrow$ Rate Limiter cho qua). Tuy nhiên, tài khoản này trong tháng đã sử dụng hết hạn mức ngân sách $10.0 USD (ví dụ đã chi tiêu $10.005 USD). Khi đó Cost Guard phát hiện vượt ngân sách tháng và lập tức chặn lại (trả về mã 402/429 "budget exceeded").
- **Tình huống Cost Guard cho qua nhưng Rate Limit chặn:**
  - Người dùng mới tạo tài khoản đầu tháng, chi phí sử dụng hiện tại là $0.00 USD (còn nguyên ngân sách $10.0 USD). Người dùng này dùng script gửi liên tục 15 request chỉ trong vòng 3 giây. Về mặt ngân sách, số token rất nhỏ không vượt trần chi tiêu (Cost Guard đồng ý), nhưng Rate Limiter sẽ can thiệp và chặn từ request thứ 11 trở đi (trả về mã 429 "rate limit exceeded") để bảo vệ server khỏi nghẽn hàng đợi.

---

### Câu 8 — /health khác /ready (CP4)

Nếu gộp hai endpoint làm một và cho nó kiểm tra Redis, chuyện gì xảy ra với cụm
3 container khi Redis mất kết nối 30 giây? Trả lời theo đúng thứ tự sự kiện.

Nếu gộp kiểm tra phụ thuộc Redis vào Liveness probe (`/health`), khi Redis mất kết nối 30 giây, chuỗi phản ứng dây chuyền thảm họa (Cascading Failure) sau sẽ xảy ra:
1. **Liveness check thất bại:** Bộ điều phối (Orchestrator như Kubernetes / Render) gửi request định kỳ tới `/health` của cả 3 container agent. Do Redis mất kết nối, cả 3 container đều trả về lỗi 503 / timeout.
2. **Orchestrator kill và restart cả cụm:** Nhận thấy liveness probe hỏng, Orchestrator kết luận ứng dụng bị deadlock/hỏng tiến trình và phát lệnh tiêu diệt (restart) cả 3 container agent.
3. **Rơi vào vòng lặp tử thần (CrashLoopBackOff):** Các container mới khởi động lại, tiếp tục kiểm tra Redis và tiếp tục fail vì Redis vẫn đang trong 30 giây gián đoạn. Chúng lại bị kill và restart lặp đi lặp lại.
4. **Mất trắng dịch vụ (Outage toàn diện):** Toàn bộ hệ thống sập hoàn toàn, mọi kết nối của khách hàng bị ngắt quãng, không còn container nào trực chiến. Khi Redis hoạt động trở lại sau 30 giây, hệ thống vẫn phải mất thêm thời gian trễ do các container đang kẹt trong chu kỳ chờ backoff.
*Nếu tách riêng chuẩn mực:* `/health` (Liveness) vẫn trả về 200 giúp container được giữ sống; chỉ có `/ready` (Readiness) trả về 503 để Load Balancer tạm thời ngắt hướng traffic người dùng vào container cho đến khi Redis kết nối lại thành công, hoàn toàn không gây crash ứng dụng.

---

### Câu 9 — Stateless (CP4)

Chạy `docker compose up --scale agent=3` rồi gọi `/ask` nhiều lần với cùng một
`X-User-Id`. Quan sát `history_length` trong response. Nếu lịch sử được lưu
trong một dict Python thay vì Redis, bạn sẽ thấy con số đó thay đổi thế nào?

- **Khi lưu trên Redis (Stateless - hệ thống hiện tại):**
  - Cả 3 container agent đều không lưu dữ liệu người dùng trong bộ nhớ nội bộ mà cùng đọc/ghi vào cơ sở dữ liệu chung Redis.
  - Dù Load Balancer phân phối các request tuần tự tới agent-1, agent-2, hay agent-3, lịch sử hội thoại vẫn được đồng bộ nhất quán: `history_length` tăng đều đặn $0 \rightarrow 2 \rightarrow 4 \rightarrow 6...$ và agent nhớ toàn bộ ngữ cảnh trước đó.
- **Nếu lưu trong dict Python (Stateful trong RAM container):**
  - Mỗi container sẽ có một dictionary riêng trong RAM của nó và không hề chia sẻ với các container khác.
  - Khi người dùng gửi liên tiếp các câu hỏi:
    - Request 1 vào `agent-1`: dict agent-1 ghi nhận, `history_length` = 0 (sau đó lưu 2 message vào RAM agent-1).
    - Request 2 bị Load Balancer chuyển sang `agent-2`: RAM của agent-2 chưa hề có user này $\rightarrow$ `history_length` bị tụt giật lùi về **0**! Agent trả lời như thể một phiên hội thoại mới tinh.
    - Request 3 chuyển sang `agent-3` $\rightarrow$ `history_length` tiếp tục là **0**.
    - Request 4 quay trở lại `agent-1` $\rightarrow$ `history_length` bất ngờ nhảy lên **2**.
  - Kết quả: `history_length` nhảy loạn xạ và ngữ cảnh bị đứt đoạn nghiêm trọng, phá vỡ hoàn toàn khả năng mở rộng ngang (Horizontal Scaling).

---

### Câu 10 — Deploy thật (CP5)

Ghi lại **một** lỗi bạn gặp khi deploy lên cloud (build fail, health check
timeout, sai REDIS_URL, app không đọc `$PORT`...): thông báo lỗi là gì, bạn
tìm ra nguyên nhân bằng cách nào, và sửa ra sao?

- **Lỗi gặp phải:** Health check timeout do không lắng nghe đúng cổng biến môi trường `$PORT` của Cloud Platform (Render).
- **Thông báo lỗi trên Cloud Logs:**
  `==> Port scan timeout reached. Port 8000 is not open or service failed to bind to 0.0.0.0:$PORT`
  (Service bị platform đánh dấu Deploy Failed và liên tục restart).
- **Cách tìm ra nguyên nhân:**
  1. Mở xem trực tiếp **Logs** trên Render Dashboard.
  2. Nhận thấy Cloud Platform không cố định cổng `8000` mà tự động cấp phát một cổng ngẫu nhiên thông qua biến môi trường `$PORT` (ví dụ `PORT=10000`).
  3. Lệnh khởi chạy nếu hardcode `--port 8000` sẽ khiến Uvicorn mở cổng 8000, trong khi bộ định tuyến (Reverse Proxy) của platform lại kiểm tra và gửi traffic tới cổng trong `$PORT`.
- **Cách sửa chữa:**
  1. Trong `app/config.py`: Khai báo `port: int = Field(default=8000, validation_alias="PORT")` để Pydantic tự động map biến môi trường `PORT` vào config.
  2. Trong `Dockerfile`: Dùng shell form cho lệnh CMD để bung giá trị biến môi trường khi container khởi chạy:
     `CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]`
  3. Sau khi sửa và đẩy code lên, Render scan đúng port mở, probe health check trả về 200 và chuyển trạng thái sang **Live**.
