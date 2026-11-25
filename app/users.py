from app.security import hash_password

# Mật khẩu demo, chỉ dùng cho bài thực hành
USERS = {
    "admin": {
        "username": "admin",
        "password_hash": hash_password("admin123"),
        "role": "staff",
    },
    "sinhvien": {
        "username": "sinhvien",
        "password_hash": hash_password("sv123456"),
        "role": "student",
    },
}


def get_user(username: str) -> dict | None:
    return USERS.get(username)
