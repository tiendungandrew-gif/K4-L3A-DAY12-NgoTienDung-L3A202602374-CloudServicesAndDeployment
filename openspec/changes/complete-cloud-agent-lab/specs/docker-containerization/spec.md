# Spec Delta: Docker Containerization

## Purpose

Đóng gói ứng dụng theo chuẩn Docker Multi-stage, bảo mật non-root user, tích hợp healthcheck và Compose multi-container.

## ADDED Requirements

### Requirement: Multi-stage Docker Build gọn nhẹ và bảo mật
`Dockerfile` MUST sử dụng multi-stage build (`AS builder` và `AS runtime` từ python:3.11-slim) để giữ dung lượng image dưới 500MB. Runtime container MUST chạy dưới quyền user không phải root (`appuser` với UID 10001), có khai báo `HEALTHCHECK` kiểm tra `/health`, và uvicorn MUST bind `0.0.0.0` và lắng nghe biến môi trường `${PORT:-8000}`.

#### Scenario: Kiểm tra dung lượng và user của Docker image
- **WHEN** build docker image `day12-agent:prod`
- **THEN** dung lượng image nhỏ hơn 500MB và process bên trong container chạy dưới quyền user `appuser`

### Requirement: Multi-container Orchestration với Docker Compose
File `docker-compose.yml` MUST định nghĩa service `agent` phụ thuộc vào `redis`, chuyển tiếp biến môi trường `AGENT_API_KEY` và `REDIS_URL=redis://redis:6379/0`, đồng thời `.dockerignore` MUST loại bỏ `.env`, `.venv`, `.git`, `__pycache__` khỏi build context.

#### Scenario: Khởi động hệ thống qua Compose
- **WHEN** thực thi `docker compose up -d`
- **THEN** service `agent` và `redis` đều khởi động thành công và liên lạc được với nhau qua mạng Docker nội bộ
