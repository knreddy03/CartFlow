from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.product import Product
from app.models.sub_category import SubCategory


DEFAULT_PRODUCTS = [
    # Men - Jackets
    {
        "subcategory_slug": "jackets",
        "name": "Classic Harrington Jacket",
        "slug": "classic-harrington-jacket",
        "description": "A lightweight jacket with a timeless silhouette.",
        "price": 9999,
        "currency": "USD",
        "stock_quantity": 25,
        "image_url": "/images/products/men/classic-harrington-jacket.jpg",
        "is_active": True,
    },

    # Accessories - Belts
    {
        "subcategory_slug": "belts",
        "name": "Classic Leather Belt",
        "slug": "classic-leather-belt",
        "description": "A timeless leather belt with a polished buckle.",
        "price": 3999,
        "currency": "USD",
        "stock_quantity": 50,
        "image_url": "https://example.com/products/classic-leather-belt.jpg",
        "is_active": True,
    },

    # Men - Shirts
    {
        "subcategory_slug": "shirts",
        "name": "Classic Oxford Shirt",
        "slug": "classic-oxford-shirt",
        "description": "A timeless Oxford shirt designed for everyday wear.",
        "price": 5999,
        "currency": "USD",
        "stock_quantity": 50,
        "image_url": "/images/products/men/classic-oxford-shirt.jpg",
        "is_active": True,
    },

    # Women - Jackets
    {
        "subcategory_slug": "women-jackets",
        "name": "Cropped Utility Jacket",
        "slug": "cropped-utility-jacket",
        "description": "A modern cropped jacket with utility-inspired details.",
        "price": 9999,
        "currency": "USD",
        "stock_quantity": 20,
        "image_url": "/images/products/women/cropped-utility-jacket.jpg",
        "is_active": True,
    },

    # Men - T-Shirts
    {
        "subcategory_slug": "t-shirts",
        "name": "Essential Cotton T-Shirt",
        "slug": "essential-cotton-t-shirt",
        "description": "A soft cotton t-shirt made for everyday comfort.",
        "price": 2999,
        "currency": "USD",
        "stock_quantity": 75,
        "image_url": "/images/products/men/essential-cotton-tshirt.jpg",
        "is_active": True,
    },
    {
        "subcategory_slug": "t-shirts",
        "name": "Premium Heavyweight T-Shirt",
        "slug": "premium-heavyweight-tshirt",
        "description": "A structured heavyweight cotton t-shirt.",
        "price": 3999,
        "currency": "USD",
        "stock_quantity": 60,
        "image_url": "/images/products/men/premium-heavyweight-tshirt.jpg",
        "is_active": True,
    },

    # Women - Dresses
    {
        "subcategory_slug": "dresses",
        "name": "Floral Midi Dress",
        "slug": "floral-midi-dress",
        "description": "A relaxed floral midi dress for effortless styling.",
        "price": 8999,
        "currency": "USD",
        "stock_quantity": 30,
        "image_url": "/images/products/women/floral-midi-dress.jpg",
        "is_active": True,
    },
    {
        "subcategory_slug": "dresses",
        "name": "Satin Evening Dress",
        "slug": "satin-evening-dress",
        "description": "An elegant satin dress designed for special occasions.",
        "price": 12999,
        "currency": "USD",
        "stock_quantity": 20,
        "image_url": "/images/products/women/satin-evening-dress.jpg",
        "is_active": True,
    },

    # Women - Jeans
    {
        "subcategory_slug": "women-jeans",
        "name": "High Rise Straight Jeans",
        "slug": "high-rise-straight-jeans",
        "description": "High-rise jeans with a modern straight-leg fit.",
        "price": 7999,
        "currency": "USD",
        "stock_quantity": 35,
        "image_url": "/images/products/women/high-rise-straight-jeans.jpg",
        "is_active": True,
    },

    # Kids - Shorts
    {
        "subcategory_slug": "kids-shorts",
        "name": "Kids Casual Shorts",
        "slug": "kids-casual-shorts",
        "description": "Comfortable casual shorts for everyday play.",
        "price": 2999,
        "currency": "USD",
        "stock_quantity": 60,
        "image_url": "https://example.com/products/kids-casual-shorts.jpg",
        "is_active": True,
    },

    # Kids - T-Shirts
    {
        "subcategory_slug": "kids-t-shirts",
        "name": "Kids Essential T-Shirt",
        "slug": "kids-essential-tshirt",
        "description": "A soft everyday t-shirt designed for kids.",
        "price": 1999,
        "currency": "USD",
        "stock_quantity": 80,
        "image_url": "https://example.com/products/kids-essential-tshirt.jpg",
        "is_active": True,
    },

    # Kids - Jeans
    {
        "subcategory_slug": "kids-jeans",
        "name": "Kids Straight Jeans",
        "slug": "kids-straight-jeans",
        "description": "Comfortable everyday denim for kids.",
        "price": 4499,
        "currency": "USD",
        "stock_quantity": 40,
        "image_url": "https://example.com/products/kids-straight-jeans.jpg",
        "is_active": True,
    },

    # Kids - Dresses
    {
        "subcategory_slug": "kids-dresses",
        "name": "Kids Summer Dress",
        "slug": "kids-summer-dress",
        "description": "A lightweight summer dress for everyday adventures.",
        "price": 3999,
        "currency": "USD",
        "stock_quantity": 45,
        "image_url": "https://example.com/products/kids-summer-dress.jpg",
        "is_active": True,
    },

    # Accessories - Hats
    {
        "subcategory_slug": "hats",
        "name": "Minimal Cotton Cap",
        "slug": "minimal-cotton-cap",
        "description": "A clean everyday cotton cap.",
        "price": 2499,
        "currency": "USD",
        "stock_quantity": 60,
        "image_url": "https://example.com/products/minimal-cotton-cap.jpg",
        "is_active": True,
    },

    # Accessories - Watches
    {
        "subcategory_slug": "watches",
        "name": "Minimal Steel Watch",
        "slug": "minimal-steel-watch",
        "description": "A minimalist stainless steel watch.",
        "price": 14999,
        "currency": "USD",
        "stock_quantity": 15,
        "image_url": "https://example.com/products/minimal-steel-watch.jpg",
        "is_active": True,
    },

    # Women - Skirts
    {
        "subcategory_slug": "skirts",
        "name": "Pleated Midi Skirt",
        "slug": "pleated-midi-skirt",
        "description": "A flowing pleated skirt for everyday elegance.",
        "price": 6499,
        "currency": "USD",
        "stock_quantity": 30,
        "image_url": "/images/products/women/pleated-midi-skirt.jpg",
        "is_active": True,
    },

    # Women - Tops
    {
        "subcategory_slug": "tops",
        "name": "Relaxed Cotton Top",
        "slug": "relaxed-cotton-top",
        "description": "A lightweight everyday cotton top.",
        "price": 3999,
        "currency": "USD",
        "stock_quantity": 50,
        "image_url": "/images/products/women/relaxed-cotton-top.jpg",
        "is_active": True,
    },
    {
        "subcategory_slug": "tops",
        "name": "Silk Blouse",
        "slug": "silk-blouse",
        "description": "A refined silk blouse with a relaxed silhouette.",
        "price": 8999,
        "currency": "USD",
        "stock_quantity": 25,
        "image_url": "/images/products/women/silk-blouse.jpg",
        "is_active": True,
    },

    # Men - Shirts
    {
        "subcategory_slug": "shirts",
        "name": "Relaxed Linen Shirt",
        "slug": "relaxed-linen-shirt",
        "description": "A lightweight linen shirt for warm-weather days.",
        "price": 6999,
        "currency": "USD",
        "stock_quantity": 35,
        "image_url": "/images/products/men/relaxed-linen-shirt.jpg",
        "is_active": True,
    },

    # Men - Jeans
    {
        "subcategory_slug": "jeans",
        "name": "Relaxed Straight Jeans",
        "slug": "relaxed-straight-jeans",
        "description": "Relaxed straight-leg denim for everyday styling.",
        "price": 8499,
        "currency": "USD",
        "stock_quantity": 30,
        "image_url": "/images/products/men/relaxed-straight-jeans.jpg",
        "is_active": True,
    },
    {
        "subcategory_slug": "jeans",
        "name": "Slim Fit Denim",
        "slug": "slim-fit-denim",
        "description": "Classic slim-fit jeans with a comfortable stretch.",
        "price": 7999,
        "currency": "USD",
        "stock_quantity": 40,
        "image_url": "/images/products/men/slim-fit-denim.jpg",
        "is_active": True,
    },

    # Accessories - Bags
    {
        "subcategory_slug": "bags",
        "name": "Structured Everyday Bag",
        "slug": "structured-everyday-bag",
        "description": "A versatile bag designed for everyday essentials.",
        "price": 8999,
        "currency": "USD",
        "stock_quantity": 25,
        "image_url": "https://example.com/products/structured-everyday-bag.jpg",
        "is_active": True,
    },

    # Men - Trousers
    {
        "subcategory_slug": "trousers",
        "name": "Tailored Chino Trousers",
        "slug": "tailored-chino-trousers",
        "description": "Versatile chinos with a refined tailored fit.",
        "price": 6499,
        "currency": "USD",
        "stock_quantity": 45,
        "image_url": "/images/products/men/tailored-chino-trousers.jpg",
        "is_active": True,
    },
]


def seed_products() -> None:
    db = SessionLocal()

    try:
        for product_data in DEFAULT_PRODUCTS:
            subcategory_slug = product_data.pop("subcategory_slug")

            subcategory = db.scalar(
                select(SubCategory).where(
                    SubCategory.slug == subcategory_slug
                )
            )

            if not subcategory:
                raise ValueError(
                    f"SubCategory '{subcategory_slug}' not found."
                )

            existing_product = db.scalar(
                select(Product).where(
                    Product.slug == product_data["slug"]
                )
            )

            if existing_product:
                print(
                    f"Product '{product_data['slug']}' "
                    "already exists. Skipping."
                )
                continue

            product = Product(
                sub_category_id=subcategory.id,
                **product_data,
            )

            db.add(product)

        db.commit()

        print("Product seeding completed successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_products()