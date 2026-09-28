# Spec Delta: 12-Factor Config, Health & Structured Logging

## Purpose

Cấu hình 12-Factor App từ môi trường, logging cấu trúc dạng JSON và liveness probe (/health) độc lập.

## ADDED Requirements

### Requirement: 12-Factor Configuration với Pydantic Settings
Hệ thống MUST tải toàn bộ cấu hình từ biến môi trường qua class `Settings` với các trường: `port` (mặc định 8000), `agent_api_key` (bắt buộc, không có giá trị mặc định), `redis_url` (mặc định `redis://localhost:6379/0`), `rate_limit_per_minute` (mặc định 10), `monthly_budget_usd` (mặc định 10.0), `log_level` (mặc định `INFO`). Nếu thiếu `AGENT_API_KEY`, ứng dụng MUST fail fast ngay khi khởi động và ném `ValidationError`.

#### Scenario: Khởi động không có AGENT_API_KEY
- **WHEN** khởi tạo `Settings` không truyền `AGENT_API_KEY` trong biến môi trường
- **THEN** ứng dụng ném lỗi `ValidationError` ngay lập tức

#### Scenario: Đọc cấu hình tùy biến từ biến môi trường
- **WHEN** các biến môi trường `PORT`, `RATE_LIMIT_PER_MINUTE`, `MONTHLY_BUDGET_USD` được set trong environment
- **THEN** đối tượng `Settings` nhận đúng các giá trị tùy biến đó mà không hardcode trong code

### Requirement: Structured Logging JSON 1 dòng
Hệ thống MUST cung cấp hàm `log_event(event, level="info", **fields)` để tạo ra 1 dòng JSON object chuẩn in ra stdout với các trường tối thiểu: `event`, `level` (viết thường), `timestamp` (ISO-8601 UTC).

#### Scenario: Ghi log JSON tiêu chuẩn
- **WHEN** hàm `log_event("ask_completed", user_id="sv01", cost_usd=0.0001)` được gọi
- **THEN** stdout nhận đúng 1 dòng JSON chứa đầy đủ các thuộc tính `event`, `level`, `timestamp`, `user_id`, `cost_usd`

### Requirement: Independent Liveness Probe /health
Endpoint `GET /health` MUST trả về HTTP 200 với `{"status": "ok", "service": "day12-agent", "version": "1.0.0"}` và MUST NOT phụ thuộc vào bất kỳ kết nối hạ tầng ngoài nào như Redis hay Database. Trường hợp ứng dụng đang dừng graceful (`lifecycle.shutting_down == True`), `/health` MUST trả về HTTP 503 với `{"status": "shutting_down"}`.

#### Scenario: Truy cập /health bình thường
- **WHEN** client gửi HTTP GET tới `/health`
- **THEN** hệ thống phản hồi status 200 và JSON body `{"status": "ok", "service": "day12-agent", "version": "1.0.0"}` không yêu cầu API Key
