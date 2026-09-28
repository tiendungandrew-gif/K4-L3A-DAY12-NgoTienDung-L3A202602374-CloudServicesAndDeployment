# Proposal: Complete Cloud Agent & Deployment Lab

## Why

Bài lab K4-L3A-DAY12 yêu cầu đưa một AI Agent từ dạng script local lên một service production-grade với đầy đủ hạ tầng Cloud, bảo mật, khả năng mở rộng (stateless scaling) và quy trình deployment an toàn. Việc thực thi theo OpenSpec giúp đảm bảo toàn bộ 5 Checkpoint (CP1-CP5), phần phản ánh (exercises.md), và Bonus CI/CD được đặc tả chính xác, đáp ứng 100% tiêu chí chấm trong `RUBRIC.md` và `LAB_GUIDE.md`.

## What Changes

- **[CP1] Config, Health & Logging (Đã hoàn thành)**: Tách config theo 12-Factor qua `Settings` (fail-fast secret), ghi log JSON 1 dòng tiêu chuẩn qua `log_event()`, và mở endpoint `/health` độc lập.
- **[CP2] Docker Containerization**: Viết `Dockerfile` multi-stage build, chạy non-root (`appuser`), tích hợp `HEALTHCHECK` & `$PORT`, bổ sung `.dockerignore`, cấu hình `docker-compose.yml` cho service `agent` và `redis`.
- **[CP3] API Security**: Xác thực API Key an toàn bằng `secrets.compare_digest`, sliding-window rate limit bằng Redis Sorted Set, cost guard theo tháng (`cost:<user>:<YYYY-MM>`), bảo vệ endpoint `/ask`.
- **[CP4] Scaling & Reliability**: Lưu lịch sử chat trên Redis (`ConversationStore` với `RPUSH`, `LTRIM`, `EXPIRE`), tạo endpoint `/ready` kiểm tra Redis `ping()`, xử lý graceful shutdown bắt tín hiệu `SIGTERM`/`SIGINT`.
- **[CP5] Cloud Deployment & Docs**: Cấu hình deployment (Railway / Render / Local Fallback), cập nhật `DEPLOYMENT.md`, lưu ảnh minh chứng `screenshots/`, vượt qua bài test `test_cp5.py`.
- **Phản ánh & Chấm điểm**: Hoàn thành 10 câu hỏi trong `exercises.md` và chạy `python grade.py` kiểm tra kết quả.
- **[Bonus] CI/CD Pipeline**: Xây dựng `.github/workflows/ci.yml` tự động chạy test, build Docker image trên GitHub Actions.

## Capabilities

### New Capabilities
- `12-factor-config-logging`: Cấu hình 12-factor, fail-fast secrets, JSON structured logging & liveness `/health`.
- `docker-containerization`: Dockerfile multi-stage, non-root user, healthcheck, `.dockerignore` và docker-compose multi-container.
- `api-security`: API Key auth (constant-time), sliding-window rate limit, monthly budget cost guard.
- `scaling-reliability`: Redis stateless conversation store, readiness probe `/ready`, graceful shutdown signal handlers.
- `cloud-deployment`: Public cloud deployment, deployment manifest, screenshots và deployment verification tests.
- `exercises-and-cicd`: 10 câu hỏi phản ảnh lý thuyết trong `exercises.md` và GitHub Actions CI/CD workflow bonus.

### Modified Capabilities
<!-- None -->

## Impact

- **Source Code (`app/`)**: `config.py`, `logging_utils.py`, `main.py`, `auth.py`, `rate_limiter.py`, `cost_guard.py`, `store.py`, `lifecycle.py`.
- **Infrastructure**: `Dockerfile`, `docker-compose.yml`, `.dockerignore`, `.env`, `.github/workflows/ci.yml`.
- **Documentation**: `DEPLOYMENT.md`, `exercises.md`, `screenshots/`.
- **Testing & Grading**: `tests/test_cp1.py` đến `test_cp5.py`, `test_bonus_cicd.py`, `grade.py`.
