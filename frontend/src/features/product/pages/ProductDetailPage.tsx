import { useParams } from "react-router-dom";

import { useProduct } from "../hooks/useProduct";
import Loader from "../../../components/common/Loader";

function formatPrice(price: number, currency: string) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
  }).format(price / 100);
}

function ProductDetailPage() {
  const { productId } = useParams<{ productId: string }>();

  const { data: product, isLoading, isError } = useProduct(productId ?? "");

  if (!productId) {
    return (
      <main
        className="min-h-screen bg-white px-5 py-24 sm:px-8 lg:px-12"
        role="main"
      >
        <div className="mx-auto max-w-[1600px] text-center space-y-4">
          <h1 className="text-3xl font-light text-gray-900">
            Product not found
          </h1>
          <p className="text-sm text-gray-600">
            This product is no longer available.
          </p>
        </div>
      </main>
    );
  }

  if (isLoading) {
    return (
      <main
        className="min-h-screen bg-white px-5 py-24 sm:px-8 lg:px-12"
        role="main"
      >
        <div className="mx-auto max-w-[1600px]">
          <div
            className="flex flex-col items-center justify-center gap-6 py-20"
            role="status"
            aria-live="polite"
          >
            <Loader size="lg" />
            <p className="text-sm text-gray-500 animate-pulse">
              Loading product details...
            </p>
          </div>
        </div>
      </main>
    );
  }

  if (isError || !product) {
    return (
      <main
        className="min-h-screen bg-white px-5 py-24 sm:px-8 lg:px-12"
        role="main"
      >
        <div className="mx-auto max-w-[1600px]">
          <div
            className="rounded-lg border border-red-200 bg-red-50 p-8 text-center space-y-3"
            role="alert"
          >
            <h1 className="text-2xl font-light text-gray-900">
              Product not found
            </h1>
            <p className="text-sm text-red-700">
              This product may have been removed or is temporarily unavailable.
            </p>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-white" role="main">
      <section className="px-5 py-16 sm:px-8 lg:px-12 lg:py-24">
        <div className="mx-auto grid max-w-[1600px] gap-10 lg:grid-cols-2 lg:gap-16">
          {/* Product Image */}
          <div className="aspect-[3/4] overflow-hidden bg-gray-100 rounded-lg shadow-sm">
            <img
              src={product.image_url}
              alt={product.name}
              className="h-full w-full object-cover"
              loading="eager"
            />
          </div>

          {/* Product Details */}
          <div className="flex flex-col justify-center space-y-8">
            {/* Header */}
            <div className="space-y-3">
              <p className="text-xs font-semibold uppercase tracking-[0.3em] text-gray-600">
                Product Details
              </p>

              <h1 className="text-4xl font-light tracking-tight text-gray-900 sm:text-5xl line-clamp-2">
                {product.name}
              </h1>
            </div>

            {/* Price */}
            <div className="border-b border-gray-200 pb-8">
              <p className="text-3xl font-light text-gray-900">
                {formatPrice(product.price, product.currency)}
              </p>
              <p className="mt-2 text-xs text-gray-600">
                Excluding taxes and shipping
              </p>
            </div>

            {/* Description */}
            {product.description && (
              <div className="border-b border-gray-200 pb-8">
                <p className="text-sm leading-relaxed text-gray-700">
                  {product.description}
                </p>
              </div>
            )}

            {/* Stock Status */}
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <div
                  className={`h-3 w-3 rounded-full ${
                    product.stock_quantity > 0 ? "bg-green-500" : "bg-red-500"
                  }`}
                />
                <p className="text-sm font-medium text-gray-900">
                  {product.stock_quantity > 0
                    ? `${product.stock_quantity} ${product.stock_quantity === 1 ? "item" : "items"} available`
                    : "Out of stock"}
                </p>
              </div>
            </div>

            {/* CTA Button Placeholder */}
            <div className="pt-4">
              <button
                className="w-full bg-gray-900 text-white px-8 py-4 rounded-lg font-semibold uppercase tracking-[0.08em] transition-all duration-200 hover:bg-gray-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-900 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                disabled={product.stock_quantity === 0}
                aria-label={
                  product.stock_quantity > 0 ? "Add to cart" : "Out of stock"
                }
              >
                {product.stock_quantity > 0 ? "Add to Cart" : "Out of Stock"}
              </button>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

export default ProductDetailPage;
