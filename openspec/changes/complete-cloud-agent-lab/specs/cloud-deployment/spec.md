# Spec Delta: Cloud Deployment

## Purpose

Triển khai ứng dụng lên nền tảng Cloud công khai (hoặc Local Fallback) và cung cấp đầy đủ minh chứng trong DEPLOYMENT.md.

## ADDED Requirements

### Requirement: Triển khai Cloud và Tài liệu Deployment
Ứng dụng MUST được triển khai lên nền tảng Cloud (Railway / Render / Cloud Run) hoặc bật `LOCAL_FALLBACK=true` nếu không dùng Cloud. File `DEPLOYMENT.md` MUST được điền đầy đủ URL HTTPS public, danh sách biến môi trường (không lộ secret), và ảnh chụp màn hình dashboard lưu trong thư mục `screenshots/`.

#### Scenario: Kiểm tra tự động CP5
- **WHEN** thực thi `pytest tests/test_cp5.py -v`
- **THEN** toàn bộ các test kiểm tra Public URL, `/health`, `/ready` và xác thực đều vượt qua thành công
