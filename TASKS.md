# Kế Hoạch Triển Khai Chi Tiết — Lab Hạ Tầng Cloud & Deployment

> **OpenSpec Change ID:** `complete-cloud-agent-lab`  
> **Thư mục tài liệu OpenSpec:** `openspec/changes/complete-cloud-agent-lab/`  
> **Tổng điểm mục tiêu:** 100/100 (Bắt buộc) + 10 (Bonus CI/CD)

---

## 🟢 Checkpoint 1 — 12-Factor Config, Health & Logging (15/15 Điểm)
*Trạng thái: **ĐÃ HOÀN THÀNH (13/13 test passed)***

- [x] **Task 1.1:** [`app/config.py`](file:///e:/Tien%20Dung/VIN/K4-L3A-DAY12-NgoTienDung-L3A202602374-CloudServicesAndDeployment/app/config.py)
  - Khai báo 6 trường: `port` (8000), `agent_api_key` (bắt buộc, không default để fail-fast), `redis_url`, `rate_limit_per_minute` (10), `monthly_budget_usd` (10.0), `log_level` ("INFO").
- [x] **Task 1.2:** [`app/logging_utils.py`](file:///e:/Tien%20Dung/VIN/K4-L3A-DAY12-NgoTienDung-L3A202602374-CloudServicesAndDeployment/app/logging_utils.py)
  - Cài đặt `log_event()` xuất ra một dòng JSON duy nhất chứa `event`, `level` viết thường, `timestamp` UTC ISO-8601.
- [x] **Task 1.3:** [`app/main.py`](file:///e:/Tien%20Dung/VIN/K4-L3A-DAY12-NgoTienDung-L3A202602374-CloudServicesAndDeployment/app/main.py)
  - Cài đặt `/health` liveness probe độc lập không phụ thuộc Redis.
- [x] **Lệnh xác thực:**
  ```powershell
  .\.venv\Scripts\pytest tests/test_cp1.py -v
  ```

---

## 🟢 Checkpoint 2 — Docker Containerization (15/15 Điểm)
*Trạng thái: **ĐÃ HOÀN THÀNH (16/16 test passed)***

- [x] **Task 2.1:** Cập nhật [`Dockerfile`](file:///e:/Tien%20Dung/VIN/K4-L3A-DAY12-NgoTienDung-L3A202602374-CloudServicesAndDeployment/Dockerfile)
  - Tách thành 2 stage: `AS builder` cài thư viện với `--prefix=/install` và `AS runtime` chỉ copy kết quả.
  - Tối ưu thứ tự layer cache: `COPY requirements.txt` trước khi `COPY app`.
  - Tạo user thường `appuser` (UID 10001), chạy lệnh bằng `USER appuser`.
  - Thêm chỉ thị `HEALTHCHECK` kiểm tra `/health`.
  - Đọc biến `$PORT` linh hoạt: `uvicorn ... --host 0.0.0.0 --port ${PORT:-8000}`.
- [x] **Task 2.2:** Cập nhật [`.dockerignore`](file:///e:/Tien%20Dung/VIN/K4-L3A-DAY12-NgoTienDung-L3A202602374-CloudServicesAndDeployment/.dockerignore)
  - Loại trừ `.env`, `.venv`, `.git`, `__pycache__`, `.pytest_cache`, `screenshots`, `openspec`.
- [x] **Task 2.3:** Cập nhật [`docker-compose.yml`](file:///e:/Tien%20Dung/VIN/K4-L3A-DAY12-NgoTienDung-L3A202602374-CloudServicesAndDeployment/docker-compose.yml)
  - Thêm service `agent` build từ `Dockerfile`, mở cổng `8000:8000`, liên kết `depends_on: redis`.
  - Truyền biến môi trường: `AGENT_API_KEY: ${AGENT_API_KEY}` và `REDIS_URL: redis://redis:6379/0`.
- [x] **Lệnh xác thực:**
  ```powershell
  .\.venv\Scripts\pytest tests/test_cp2.py -v
  ```


---

## 🟢 Checkpoint 3 — API Security (20/20 Điểm)
*Trạng thái: **ĐÃ HOÀN THÀNH (22/22 test passed)***

- [x] **Task 3.1:** Cài đặt xác thực `X-API-Key` với `secrets.compare_digest` chống Timing Attack trong [`app/auth.py`](file:///e:/Tien%20Dung/VIN/K4-L3A-DAY12-NgoTienDung-L3A202602374-CloudServicesAndDeployment/app/auth.py).
- [x] **Task 3.2:** Cài đặt Sliding-window Rate Limiting dựa trên Redis Sorted Set trong [`app/rate_limiter.py`](file:///e:/Tien%20Dung/VIN/K4-L3A-DAY12-NgoTienDung-L3A202602374-CloudServicesAndDeployment/app/rate_limiter.py).
- [x] **Task 3.3:** Cài đặt Monthly Budget Cost Guard kiểm tra chi phí theo `cost:<user>:<YYYY-MM>` trong [`app/cost_guard.py`](file:///e:/Tien%20Dung/VIN/K4-L3A-DAY12-NgoTienDung-L3A202602374-CloudServicesAndDeployment/app/cost_guard.py).
- [x] **Task 3.4:** Tích hợp kiểm tra an ninh theo thứ tự trong `/ask` ([`app/main.py`](file:///e:/Tien%20Dung/VIN/K4-L3A-DAY12-NgoTienDung-L3A202602374-CloudServicesAndDeployment/app/main.py)).
- [x] **Lệnh xác thực:**
  ```powershell
  .\.venv\Scripts\pytest tests/test_cp3.py -v
  ```


---

## 🟢 Checkpoint 4 — Scaling & Reliability (20/20 Điểm)
*Trạng thái: **ĐÃ HOÀN THÀNH (19/19 test passed)***

- [x] **Task 4.1:** Cài đặt [`app/store.py`](file:///e:/Tien%20Dung/VIN/K4-L3A-DAY12-NgoTienDung-L3A202602374-CloudServicesAndDeployment/app/store.py)
  - Lưu tin nhắn vào Redis bằng `RPUSH history:<user_id>`.
  - Giới hạn độ dài với `ltrim(key, -HISTORY_MAX_MESSAGES, -1)` và gia hạn `expire(key, HISTORY_TTL_SECONDS)`.
  - Hàm `ping()` nuốt mọi ngoại lệ và trả `bool`.
- [x] **Task 4.2:** Cài đặt `/ready` probe trong [`app/main.py`](file:///e:/Tien%20Dung/VIN/K4-L3A-DAY12-NgoTienDung-L3A202602374-CloudServicesAndDeployment/app/main.py)
  - Trả về 503 nếu `shutting_down` hoặc `store.ping() == False`; 200 `{"status": "ready", "redis": true}` khi sẵn sàng.
- [x] **Task 4.3:** Cài đặt [`app/lifecycle.py`](file:///e:/Tien%20Dung/VIN/K4-L3A-DAY12-NgoTienDung-L3A202602374-CloudServicesAndDeployment/app/lifecycle.py)
  - Bắt tín hiệu `SIGTERM` và `SIGINT`, set `shutting_down = True`, và gọi tiếp handler cũ của uvicorn.
- [x] **Lệnh xác thực:**
  ```powershell
  .\.venv\Scripts\pytest tests/test_cp4.py -v
  ```


---

## 🟢 Checkpoint 5 — Cloud Deployment (15/15 Điểm)
*Trạng thái: **ĐÃ HOÀN THÀNH (9/9 test passed, 4 skipped fallback)***

- [x] **Task 5.1:** Triển khai dịch vụ lên Cloud Render với Public URL: `https://day12-agent-5fl2.onrender.com`.
- [x] **Task 5.2:** Điền thông tin vào [`DEPLOYMENT.md`](file:///e:/Tien%20Dung/VIN/K4-L3A-DAY12-NgoTienDung-L3A202602374-CloudServicesAndDeployment/DEPLOYMENT.md) (Public URL, platform, output kiểm thử curl).
- [x] **Task 5.3:** Lưu ảnh chụp màn hình dashboard và health check vào thư mục `screenshots/`.
- [x] **Lệnh xác thực:**
  ```powershell
  .\.venv\Scripts\pytest tests/test_cp5.py -v
  ```

---

## 🟢 Phiếu Phản Ánh & Bonus CI/CD (25/25 Điểm)
*Trạng thái: **ĐÃ HOÀN THÀNH (10/10 câu hỏi + CI/CD Workflow sẵn sàng)***

- [x] **Task 6.1:** Trả lời 10 câu hỏi trong [`exercises.md`](file:///e:/Tien%20Dung/VIN/K4-L3A-DAY12-NgoTienDung-L3A202602374-CloudServicesAndDeployment/exercises.md) (15/15 Điểm)
  - Câu 1: Fail-fast trong Settings
  - Câu 2: Structured logging
  - Câu 3: Kích thước Docker Image
  - Câu 4: Thứ tự lệnh Dockerfile & Cache
  - Câu 5: Rủi ro chạy quyền root
  - Câu 6: Lợi ích của Sliding Window
  - Câu 7: Khác biệt Rate Limit vs Cost Guard
  - Câu 8: Phân biệt `/health` vs `/ready`
  - Câu 9: Tính chất Stateless Service
  - Câu 10: Xử lý lỗi khi deploy
- [x] **Task 6.2:** Xây dựng GitHub Actions CI/CD Pipeline (Bonus +10 Điểm)
  - Tạo file `.github/workflows/ci.yml` tự động chạy test, build docker image và deploy khi push/PR vào `main`.
  - Thêm CI badge vào `README.md`.
  - Xác thực qua: `.\.venv\Scripts\pytest tests/test_bonus_cicd.py -v -k "not test_badge_bao_passing"`.
- [x] **Task 6.3:** Kiểm tra tổng điểm bằng `grade.py`
  - Đạt điểm tối đa: **100.0/100 (Bắt buộc) + 10/10 (Bonus CI/CD)**.

