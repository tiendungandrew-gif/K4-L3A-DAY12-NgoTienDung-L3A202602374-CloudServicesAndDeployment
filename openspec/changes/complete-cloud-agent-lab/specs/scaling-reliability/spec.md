# Spec Delta: Scaling & Reliability

## Purpose

Thiết kế stateless service qua Redis conversation store, liveness/readiness probe độc lập và graceful shutdown.

## ADDED Requirements

### Requirement: Redis Stateless Conversation Store
Lịch sử trò chuyện MUST được lưu tập trung trên Redis (`history:<user_id>`) thay vì RAM local. Lịch sử chat MUST được giới hạn tối đa `HISTORY_MAX_MESSAGES` tin nhắn gần nhất bằng `ltrim` và tự đặt thời gian hết hạn `expire`.

#### Scenario: Truy cập lịch sử đồng bộ trên nhiều instance
- **WHEN** client gửi các câu hỏi liên tiếp được điều hướng tới các container agent khác nhau
- **THEN** lịch sử hội thoại vẫn liên tục và nhất quán nhờ bộ lưu trữ Redis chung

### Requirement: Dependency Readiness Probe /ready
Endpoint `GET /ready` MUST kiểm tra trạng thái kết nối tới Redis bằng `store.ping()`. Trả về HTTP 200 `{"status": "ready", "redis": True}` khi Redis hoạt động, và HTTP 503 `{"status": "not ready", "redis": False}` khi mất kết nối hoặc khi server đang shutting down.

#### Scenario: Kiểm tra Readiness khi Redis tạm ngừng
- **WHEN** Redis server bị ngắt kết nối
- **THEN** `/ready` trả về HTTP 503 còn `/health` vẫn trả về HTTP 200

### Requirement: Graceful Shutdown Signal Handling
Hệ thống MUST đăng ký handler bắt tín hiệu `SIGTERM` và `SIGINT`, đặt cờ `shutting_down = True`, và ủy quyền lại cho signal handler gốc của uvicorn để không cắt ngang request đang xử lý.

#### Scenario: Nhận tín hiệu SIGTERM khi deploy
- **WHEN** process nhận tín hiệu SIGTERM từ orchestrator
- **THEN** ứng dụng chuyển `/health` và `/ready` sang HTTP 503 và hoàn thành nốt request dở trước khi tắt
