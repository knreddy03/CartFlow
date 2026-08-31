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
    <Link
      to={`/products/${product.id}`}
      className="group block focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-900 focus-visible:ring-offset-2 rounded-lg transition-transform duration-300 hover:shadow-md"
      aria-label={`View ${product.name} - ${formatPrice(product.price, product.currency)}`}
    >
      <div className="relative aspect-[3/4] overflow-hidden bg-gray-100 rounded-lg">
        <img
          src={product.image_url}
          alt={product.name}
          className="h-full w-full object-cover transition-transform duration-700 ease-out group-hover:scale-105"
          loading="lazy"
        />

        {!product.is_active && (
          <div className="absolute left-4 top-4 bg-white px-3 py-1.5 text-xs font-semibold uppercase tracking-[0.15em] text-gray-900 rounded-md shadow-sm">
            Unavailable
          </div>
        )}

        <div className="absolute bottom-4 right-4 flex h-10 w-10 items-center justify-center rounded-full bg-white opacity-0 transition-all duration-300 group-hover:opacity-100 shadow-lg">
          <ArrowUpRight className="h-4 w-4 text-gray-900 transition-transform duration-300 group-hover:rotate-45" />
        </div>
      </div>

      <div className="pt-4">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <h3 className="text-sm font-semibold uppercase tracking-[0.08em] text-gray-900 line-clamp-2 group-hover:text-gray-700 transition-colors duration-200">
              {product.name}
            </h3>

            {product.description && (
              <p className="mt-1 line-clamp-1 text-xs text-gray-600">
                {product.description}
              </p>
            )}
          </div>

          <p className="shrink-0 text-sm font-semibold text-gray-900 whitespace-nowrap">
            {formatPrice(product.price, product.currency)}
          </p>
        </div>
      </div>
    </Link>
  );
}

export default ProductCard;
