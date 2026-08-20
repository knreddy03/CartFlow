import { useParams } from "react-router-dom";

import { useProduct } from "../hooks/useProduct";

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
    return <p>Product not found.</p>;
  }

  if (isLoading) {
    return (
      <main className="min-h-screen bg-[#f8f7f4] px-5 py-24 sm:px-8 lg:px-12">
        <p className="text-sm text-neutral-500">Loading product...</p>
      </main>
    );
  }

  if (isError || !product) {
    return (
      <main className="min-h-screen bg-[#f8f7f4] px-5 py-24 sm:px-8 lg:px-12">
        <h1 className="text-3xl font-light">Product not found.</h1>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[#f8f7f4]">
      <section className="px-5 py-16 sm:px-8 lg:px-12 lg:py-24">
        <div className="mx-auto grid max-w-[1600px] gap-10 lg:grid-cols-2 lg:gap-16">
          <div className="aspect-[3/4] overflow-hidden bg-neutral-100">
            <img
              src={product.image_url}
              alt={product.name}
              className="h-full w-full object-cover"
            />
          </div>

          <div className="flex flex-col justify-center">
            <p className="text-xs uppercase tracking-[0.3em] text-neutral-500">
              Product
            </p>

            <h1 className="mt-4 text-4xl font-light tracking-tight sm:text-5xl">
              {product.name}
            </h1>

            <p className="mt-5 text-xl">
              {formatPrice(product.price, product.currency)}
            </p>

            {product.description && (
              <p className="mt-6 max-w-lg text-sm leading-relaxed text-neutral-500">
                {product.description}
              </p>
            )}

            <div className="mt-8">
              <p className="text-sm text-neutral-500">
                {product.stock_quantity > 0
                  ? `${product.stock_quantity} available`
                  : "Out of stock"}
              </p>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

export default ProductDetailPage;
