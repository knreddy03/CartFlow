from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.category import Category


DEFAULT_CATEGORIES = [
    {
        "name": "Men",
        "slug": "men",
        "description": "Men's clothing and fashion.",
        "image_url": "...",
        "is_active": True,
    },
    {
        "name": "Women",
        "slug": "women",
        "description": "Women's clothing and fashion.",
        "image_url": "...",
        "is_active": True,
    },
    {
        "name": "Kids",
        "slug": "kids",
        "description": "Clothing and fashion for kids.",
        "image_url": "...",
        "is_active": True,
    },
    {
        "name": "Accessories",
        "slug": "accessories",
        "description": "Fashion accessories.",
        "image_url": "...",
        "is_active": True,
    },
]


def seed_categories() -> None:
    db = SessionLocal()

    try:
        for category_data in DEFAULT_CATEGORIES:
            existing_category = db.scalar(
                select(Category).where(
                    Category.slug == category_data["slug"]
                )
            )

            if existing_category:
                print(
                    f"Category '{category_data['slug']}' already exists. Skipping."
                )
                continue

            category = Category(**category_data)

            db.add(category)

        db.commit()

        print("Category seeding completed successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_categories()