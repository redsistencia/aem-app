from db.session import SessionLocal
from models.user import User, UserRole
from security.hash import hash_password

def create_admin():
    db = SessionLocal()
    try:
        password_plain = "admin123"

        admin = User(
            username="admin",
            email="admin@example.com",
            password=hash_password(password_plain),
            role=UserRole.admin,
            active=True,
        )

        db.add(admin)
        db.commit()
        print("✅ Admin creado")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
