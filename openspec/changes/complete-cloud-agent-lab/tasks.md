# Tasks

## 1. CP1 — 12-Factor Config, Health & Logging

- [x] 1.1 Khai báo 6 trường cấu hình trong `app/config.py` với `agent_api_key` không default để fail-fast.
- [x] 1.2 Cài đặt `log_event()` trong `app/logging_utils.py` ghi log một dòng JSON ra stdout.
- [x] 1.3 Cài đặt `/health` probe độc lập không phụ thuộc Redis trong `app/main.py`.
- [x] 1.4 Xác thực `pytest tests/test_cp1.py -v` đạt 13/13 test.

## 2. CP2 — Docker & Docker Compose

- [x] 2.1 Cập nhật `Dockerfile` sang multi-stage build (`AS builder` và `AS runtime`), tạo `appuser` non-root, thêm `HEALTHCHECK` và nhận biến `${PORT:-8000}`.
- [x] 2.2 Cập nhật `.dockerignore` loại trừ `.env`, `.venv`, `.git`, `__pycache__`.
- [x] 2.3 Cấu hình `docker-compose.yml` cho service `agent` liên kết tới `redis`.
- [x] 2.4 Xác thực với `pytest tests/test_cp2.py -v -m "not docker"` và `pytest tests/test_cp2.py -v`.


## 3. CP3 — API Security (Auth, Rate Limit, Cost Guard)

- [ ] 3.1 Cài đặt `app/auth.py` kiểm tra header `X-API-Key` với `secrets.compare_digest` chống timing attack.
- [ ] 3.2 Cài đặt `app/rate_limiter.py` với cửa sổ trượt Redis Sorted Set (`zremrangebyscore`, `zcard`, `zadd`, `expire`).
- [ ] 3.3 Cài đặt `app/cost_guard.py` quản lý tổng chi tiêu người dùng hàng tháng theo key `cost:<user>:<YYYY-MM>`.
- [ ] 3.4 Bọc các kiểm tra an ninh trước khi gọi LLM trong `/ask` (`app/main.py`) và xác nhận qua `pytest tests/test_cp3.py -v`.

## 4. CP4 — Scaling & Reliability (Stateless Store, Readiness, Shutdown)

- [ ] 4.1 Cài đặt `app/store.py` lưu lịch sử trò chuyện trong Redis (`history:<user_id>`) kèm `RPUSH`, `LTRIM` và `EXPIRE`.
- [ ] 4.2 Cài đặt `/ready` endpoint kiểm tra cờ `shutting_down` và kết nối Redis qua `store.ping()`.
- [ ] 4.3 Cài đặt `app/lifecycle.py` bắt các tín hiệu `SIGTERM`/`SIGINT` phục vụ Graceful Shutdown.
- [ ] 4.4 Kiểm tra toàn bộ bằng `pytest tests/test_cp4.py -v`.

## 5. CP5 — Cloud Deployment & Documentation

- [ ] 5.1 Cấu hình triển khai ứng dụng lên Cloud (Railway / Render / Local Fallback với `LOCAL_FALLBACK=true`).
- [ ] 5.2 Hoàn thiện `DEPLOYMENT.md` và chụp ảnh giao diện lưu vào `screenshots/`.
- [ ] 5.3 Xác nhận bản triển khai qua `pytest tests/test_cp5.py -v`.

## 6. Phản Ánh & Bonus CI/CD

- [ ] 6.1 Trả lời đủ 10 câu hỏi tự luận trong `exercises.md`.
- [ ] 6.2 Xây dựng workflow GitHub Actions tại `.github/workflows/ci.yml` và kiểm tra qua `pytest tests/test_bonus_cicd.py -v`.
- [ ] 6.3 Chạy lệnh `python grade.py` tự chấm điểm tổng thể đạt điểm tối đa.
