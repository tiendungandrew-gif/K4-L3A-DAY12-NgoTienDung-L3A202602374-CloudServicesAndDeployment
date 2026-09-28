# Spec Delta: API Security

## Purpose

Bảo vệ API Agent qua 3 lớp: Authentication (API Key constant-time), Rate Limiting (Sliding-window Redis), và Cost Guard (Ngân sách hàng tháng).

## ADDED Requirements

### Requirement: Constant-time API Key Verification
Hệ thống MUST xác thực header `X-API-Key` cho endpoint `/ask` bằng hàm `secrets.compare_digest` để chống tấn công Timing Attack. Nếu key không khớp hoặc thiếu, ứng dụng MUST trả về HTTP 401 Unauthorized.

#### Scenario: Gửi request không có API Key
- **WHEN** client gửi POST request đến `/ask` không kèm header `X-API-Key`
- **THEN** ứng dụng trả về HTTP 401 ngay lập tức

### Requirement: Sliding-window Rate Limiter qua Redis Sorted Set
Hệ thống MUST triển khai rate limit cửa sổ trượt bằng Redis Sorted Set (`zremrangebyscore`, `zcard`, `zadd`, `expire`). Nếu số request trong 60s vượt mức `RATE_LIMIT_PER_MINUTE`, ứng dụng MUST trả về HTTP 429 Too Many Requests.

#### Scenario: Vượt giới hạn Rate Limit
- **WHEN** một user gửi nhiều hơn 10 request trong vòng 60 giây
- **THEN** các request thứ 11 trở đi trả về HTTP 429

### Requirement: Monthly Budget Cost Guard
Hệ thống MUST theo dõi tổng chi phí LLM theo `cost:<user_id>:<YYYY-MM>`. Trước khi gọi LLM, nếu chi phí hiện tại vượt `MONTHLY_BUDGET_USD`, ứng dụng MUST trả về HTTP 402 Payment Required.

#### Scenario: Vượt ngân sách hàng tháng
- **WHEN** tổng chi phí của user vượt mức `MONTHLY_BUDGET_USD`
- **THEN** request `/ask` bị chặn trước khi gọi LLM và trả về HTTP 402
