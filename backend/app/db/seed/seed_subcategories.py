from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.category import Category
from app.models.sub_category import SubCategory


DEFAULT_SUBCATEGORIES = [
    # Accessories
    {
        "category_slug": "accessories",
        "name": "Bags",
        "slug": "bags",
        "description": "Fashion bags and everyday carry.",
        "image_url": "...",
        "is_active": True,
    },
    {
        "category_slug": "accessories",
        "name": "Belts",
        "slug": "belts",
        "description": "Fashion belts and accessories.",
        "image_url": "...",
        "is_active": True,
    },
    {
        "category_slug": "accessories",
        "name": "Hats",
        "slug": "hats",
        "description": "Hats and headwear.",
        "image_url": "...",
        "is_active": True,
    },
    {
        "category_slug": "accessories",
        "name": "Watches",
        "slug": "watches",
        "description": "Watches and wrist accessories.",
        "image_url": "...",
        "is_active": True,
    },

    # Kids
    {
        "category_slug": "kids",
        "name": "Dresses",
        "slug": "kids-dresses",
        "description": "Kids' dresses and outfits.",
        "image_url": "...",
        "is_active": True,
    },
    {
        "category_slug": "kids",
        "name": "Jeans",
        "slug": "kids-jeans",
        "description": "Kids' jeans and denim.",
        "image_url": "...",
        "is_active": True,
    },
    {
        "category_slug": "kids",
        "name": "Shorts",
        "slug": "kids-shorts",
        "description": "Kids' shorts and casual bottoms.",
        "image_url": "...",
        "is_active": True,
    },
    {
        "category_slug": "kids",
        "name": "T-Shirts",
        "slug": "kids-t-shirts",
        "description": "Kids' t-shirts and casual tops.",
        "image_url": "...",
        "is_active": True,
    },

    # Men
    {
        "category_slug": "men",
        "name": "Jackets",
        "slug": "jackets",
        "description": "Men's jackets and outerwear.",
        "image_url": "...",
        "is_active": True,
    },
    {
        "category_slug": "men",
        "name": "Jeans",
        "slug": "jeans",
        "description": "Men's jeans and denim.",
        "image_url": "...",
        "is_active": True,
    },
    {
        "category_slug": "men",
        "name": "Shirts",
        "slug": "shirts",
        "description": "Men's shirts and casual tops.",
        "image_url": "...",
        "is_active": True,
    },
    {
        "category_slug": "men",
        "name": "T-Shirts",
        "slug": "t-shirts",
        "description": "Men's t-shirts and casual wear.",
        "image_url": "...",
        "is_active": True,
    },
    {
        "category_slug": "men",
        "name": "Trousers",
        "slug": "trousers",
        "description": "Men's trousers and formal pants.",
        "image_url": "...",
        "is_active": True,
    },

    # Women
    {
        "category_slug": "women",
        "name": "Dresses",
        "slug": "dresses",
        "description": "Women's dresses and one-piece outfits.",
        "image_url": "...",
        "is_active": True,
    },
    {
        "category_slug": "women",
        "name": "Jackets",
        "slug": "women-jackets",
        "description": "Women's jackets and outerwear.",
        "image_url": "...",
        "is_active": True,
    },
    {
        "category_slug": "women",
        "name": "Jeans",
        "slug": "women-jeans",
        "description": "Women's jeans and denim.",
        "image_url": "...",
        "is_active": True,
    },
    {
        "category_slug": "women",
        "name": "Skirts",
        "slug": "skirts",
        "description": "Women's skirts and casual bottoms.",
        "image_url": "...",
        "is_active": True,
    },
    {
        "category_slug": "women",
        "name": "Tops",
        "slug": "tops",
        "description": "Women's tops and casual shirts.",
        "image_url": "...",
        "is_active": True,
    },
]


def seed_subcategories() -> None:
    db = SessionLocal()

    try:
        for subcategory_data in DEFAULT_SUBCATEGORIES:
            category_slug = subcategory_data.pop("category_slug")

            category = db.scalar(
                select(Category).where(
                    Category.slug == category_slug
                )
            )

            if not category:
                raise ValueError(
                    f"Category '{category_slug}' not found."
                )

            existing_subcategory = db.scalar(
                select(SubCategory).where(
                    SubCategory.slug == subcategory_data["slug"]
                )
            )

            if existing_subcategory:
                print(
                    f"SubCategory '{subcategory_data['slug']}' "
                    "already exists. Skipping."
                )
                continue

            subcategory = SubCategory(
                category_id=category.id,
                **subcategory_data,
            )

            db.add(subcategory)

        db.commit()

        print("SubCategory seeding completed successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_subcategories()