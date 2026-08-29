from datetime import date
from getpass import getpass
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.user import User, UserRole


def create_admin() -> None:
    db = SessionLocal()

    try:
        email = input("Admin email: ").strip().lower()
        password = getpass("Admin password: ")
        confirm_password = getpass("Confirm admin password: ")

        if password != confirm_password:
            raise ValueError("Passwords do not match.")

        existing_user = db.query(User).filter(User.email == email).first()

        if existing_user:
            print(f"User with email {email} already exists.")
            return

        mobile = input("Admin mobile: ").strip()
        first_name = input("First name: ").strip()
        last_name = input("Last name: ").strip()

        date_of_birth = date.fromisoformat(
            input("Date of birth (YYYY-MM-DD): ").strip()
        )

        admin = User(
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            email=email,
            password=hash_password(password),
            date_of_birth=date_of_birth,
            role=UserRole.ADMIN,
            is_verified=True,
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print(f"Admin user created successfully: {admin.email}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()