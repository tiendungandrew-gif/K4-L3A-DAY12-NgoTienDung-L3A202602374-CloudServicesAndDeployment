# Design: Complete Cloud Agent & Deployment Lab Architecture

## Context

Ứng dụng FastAPI AI Agent cần đáp ứng các tiêu chuẩn sản xuất (production-ready) với kiến trúc Stateless Server, Dockerization tối ưu, Security Guards và Health Monitoring. Mọi chi tiết yêu cầu được quy định chi tiết tại `LAB_GUIDE.md` và `RUBRIC.md`.

## Goals / Non-Goals

**Goals:**
- Triển khai toàn bộ 5 Checkpoints theo chuẩn REST API FastAPI.
- Xây dựng Docker Image multi-stage < 500MB, non-root user `appuser`.
- Thiết kế security layer trên Redis (API Key auth constant-time, Rate Limiting sliding window, Cost Guard).
- Tách biệt Liveness Probe (`/health`) và Readiness Probe (`/ready`).
- Tích hợp Graceful Shutdown bắt tín hiệu OS `SIGTERM`/`SIGINT`.
- Cấu hình Cloud deployment (Railway / Render / Local Fallback) và tài liệu `DEPLOYMENT.md`.
- Điền phiếu phản ánh `exercises.md` & dựng GitHub Actions CI/CD workflow.

**Non-Goals:**
- Tích hợp nhà cung cấp LLM thật (sử dụng `mock_llm.py` theo yêu cầu bài lab).
- Thay thế Redis bằng SQL Database.

## Decisions

### Decision 1: Cấu hình 12-Factor với Pydantic Settings
- **Lựa chọn**: Sử dụng `pydantic-settings` với `BaseSettings`.
- **Lý do**: Tự động chuyển đổi kiểu dữ liệu từ `os.environ`, hỗ trợ `.env` file và báo lỗi `ValidationError` ngay khi thiếu `AGENT_API_KEY` (Fail-Fast).
- **Lựa chọn thay thế cân nhắc**: Đọc `os.getenv()` thủ công — bị rủi ro bỏ sót kiểm tra kiểu dữ liệu và thiếu cơ chế fail-fast khi khởi động.

### Decision 2: Docker Multi-Stage Build & Security
- **Lựa chọn**: 
  - Stage 1 `builder` (`python:3.11-slim`): cài đặt wheels/dependencies.
  - Stage 2 `runtime` (`python:3.11-slim`): copy duy nhất site-packages và source code.
  - Tạo non-root user `appuser` (UID 10001) và chuyển `USER appuser`.
  - Tích hợp `HEALTHCHECK` gọi URL `/health`.
- **Lý do**: Giảm kích thước image từ ~1GB xuống < 200MB và nâng cao bảo mật rủi ro chiếm quyền host.

### Decision 3: Redis Sliding-Window Rate Limiting
- **Lựa chọn**: Dùng Redis Sorted Set (`ZREMRANGEBYSCORE`, `ZCARD`, `ZADD`, `EXPIRE`).
- **Lý do**: Khắc phục lỗ hổng của Fixed Window Rate Limiting (gửi dồn request ở ranh giới giữa 2 phút). Mỗi member được gán UUID duy nhất để tránh bị ghi đè khi cùng timestamp.

### Decision 4: Phân tách Liveness / Readiness Probes & Graceful Shutdown
- **Lựa chọn**:
  - `/health` (Liveness): Kiểm tra cờ `shutting_down`, trả 200/503. Không phụ thuộc Redis để tránh restart cascade khi Redis sập ngắn hạn.
  - `/ready` (Readiness): Kiểm tra cờ `shutting_down` và kết nối Redis qua `store.ping()`. Trả 200/503 để Load Balancer tự điều hướng traffic.
  - Signal Handler: Lưu lại handler cũ trong `_previous[sig]`, bật cờ `shutting_down = True` và gọi chuyển tiếp sang handler gốc của uvicorn.

## Risks / Trade-offs

- **[Risk 1: Redis Temporary Downtime]** → Mitigated by keeping `/health` independent of Redis so containers are not killed by orchestrators during Redis restarts.
- **[Risk 2: Multi-instance chat history desync]** → Mitigated by storing all conversation messages in Redis (`history:<user_id>`) with `RPUSH`, `LTRIM` and `EXPIRE`.
- **[Risk 3: Environment Secret Leakage]** → Mitigated by strictly adding `.env` into `.dockerignore` and `.gitignore`.
