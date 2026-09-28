# Spec Delta: Exercises and CI/CD Pipeline

## Purpose

Hoàn thành 10 câu hỏi tự luận phản ánh trong exercises.md và xây dựng quy trình CI/CD tự động bằng GitHub Actions.

## ADDED Requirements

### Requirement: Hoàn thiện Phiếu Phản Ánh exercises.md
File `exercises.md` MUST được hoàn thiện đầy đủ 10 câu hỏi trả lời tự luận dựa trên kết quả quan sát thực tế khi làm bài.

#### Scenario: Chấm điểm bài phản ánh
- **WHEN** thực thi `python grade.py`
- **THEN** script ghi nhận đủ 10/10 câu trả lời đã được điền.

### Requirement: Bonus GitHub Actions CI/CD Workflow
Tạo file `.github/workflows/ci.yml` tự động kích hoạt khi `push` hoặc `pull_request` vào nhánh `main`. Workflow MUST thực hiện checkout code, cài đặt môi trường, chạy `pytest` và build Docker image.

#### Scenario: Kiểm tra tự động Bonus CI/CD
- **WHEN** thực thi `pytest tests/test_bonus_cicd.py -v`
- **THEN** các test kiểm tra sự tồn tại và cú pháp hợp lệ của file workflow CI/CD đều vượt qua.
