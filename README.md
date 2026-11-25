# Canteen API

API thực đơn căng tin trường (FastAPI), có đăng nhập JWT.

## Chạy trên máy
    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env     # rồi đặt SECRET_KEY thật vào .env
    python3 -m uvicorn app.main:app --reload

Mở http://127.0.0.1:8000/docs

## Tài khoản demo
- `admin` / `admin123` (nhân viên, được thêm/sửa/xóa món)
- `sinhvien` / `sv123456` (sinh viên, chỉ xem)

## Kiểm thử
    python3 -m pytest -v
