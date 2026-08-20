import { ArrowUpRight } from "lucide-react";
import { Link } from "react-router-dom";

import type { Product } from "../product.types";

interface ProductCardProps {
  product: Product;
}

function formatPrice(price: number, currency: string) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
  }).format(price / 100);
}

function ProductCard({ product }: ProductCardProps) {
  return (
    <Link to={`/products/${product.id}`} className="group block">
      <div className="relative aspect-[3/4] overflow-hidden bg-neutral-100">
        <img
          src={product.image_url}
          alt={product.name}
          className="h-full w-full object-cover transition-transform duration-700 ease-out group-hover:scale-105"
        />

        {!product.is_active && (
          <div className="absolute left-4 top-4 bg-white px-3 py-1 text-xs uppercase tracking-[0.15em]">
            Unavailable
          </div>
        )}

        <div className="absolute bottom-4 right-4 flex h-10 w-10 items-center justify-center rounded-full bg-white opacity-0 transition-all duration-300 group-hover:opacity-100">
          <ArrowUpRight className="h-4 w-4" />
        </div>
      </div>

      <div className="pt-4">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h3 className="text-sm font-medium text-neutral-900">
              {product.name}
            </h3>

            {product.description && (
              <p className="mt-1 line-clamp-1 text-sm text-neutral-500">
                {product.description}
              </p>
            )}
          </div>

          <p className="shrink-0 text-sm text-neutral-900">
            {formatPrice(product.price, product.currency)}
          </p>
        </div>
      </div>
    </Link>
  );
}

export default ProductCard;
