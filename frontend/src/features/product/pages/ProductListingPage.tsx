import { useParams } from "react-router-dom";

import ProductGrid from "../components/ProductGrid";
import { useProducts } from "../hooks/useProducts";

function ProductListingPage() {
  const { subCategoryId } = useParams<{
    subCategoryId: string;
  }>();

  const { data, isLoading, isError } = useProducts({
    sub_category_id: subCategoryId,
    is_active: true,
    page: 1,
    page_size: 12,
  });

  if (!subCategoryId) {
    return (
      <main className="min-h-screen bg-[#f8f7f4] px-5 py-24 sm:px-8 lg:px-12">
        <div className="mx-auto max-w-[1600px]">
          <h1 className="text-3xl font-light">Collection not found.</h1>
        </div>
      </main>
    );
  }

  if (isLoading) {
    return (
      <main className="min-h-screen bg-[#f8f7f4] px-5 py-24 sm:px-8 lg:px-12">
        <div className="mx-auto max-w-[1600px]">
          <p className="text-sm text-neutral-500">Loading products...</p>
        </div>
      </main>
    );
  }

  if (isError || !data) {
    return (
      <main className="min-h-screen bg-[#f8f7f4] px-5 py-24 sm:px-8 lg:px-12">
        <div className="mx-auto max-w-[1600px]">
          <p className="text-sm text-neutral-500">Unable to load products.</p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[#f8f7f4]">
      <section className="px-5 pb-12 pt-24 sm:px-8 lg:px-12 lg:pb-16 lg:pt-32"></section>

      <section className="px-5 pb-24 sm:px-8 lg:px-12 lg:pb-32">
        <div className="mx-auto max-w-[1600px]">
          {data.items.length === 0 ? (
            <p className="text-sm text-neutral-500">
              No products available in this collection.
            </p>
          ) : (
            <ProductGrid products={data.items} />
          )}
        </div>
      </section>
    </main>
  );
}

export default ProductListingPage;
