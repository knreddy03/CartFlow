import { useParams } from "react-router-dom";

import ProductGrid from "../components/ProductGrid";
import { useProducts } from "../hooks/useProducts";
import Loader from "../../../components/common/Loader";

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
      <main
        className="min-h-screen bg-white px-5 py-24 sm:px-8 lg:px-12"
        role="main"
      >
        <div className="mx-auto max-w-[1600px] text-center space-y-4">
          <h1 className="text-3xl font-light text-gray-900">
            Collection not found
          </h1>
          <p className="text-sm text-gray-600">
            This collection is no longer available.
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
              Loading products...
            </p>
          </div>
        </div>
      </main>
    );
  }

  if (isError || !data) {
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
            <p className="text-base font-semibold text-red-800">
              Unable to load products
            </p>
            <p className="text-sm text-red-700">
              Please try refreshing the page or contact support if the problem
              persists.
            </p>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-white" role="main">
      <section className="px-5 pb-12 pt-24 sm:px-8 lg:px-12 lg:pb-16 lg:pt-32"></section>

      <section className="px-5 pb-24 sm:px-8 lg:px-12 lg:pb-32">
        <div className="mx-auto max-w-[1600px]">
          {data.items.length === 0 ? (
            <div className="rounded-lg border border-gray-200 bg-gray-50 p-8 text-center space-y-2">
              <p className="text-base font-semibold text-gray-900">
                No products available
              </p>
              <p className="text-sm text-gray-600">
                No products available in this collection.
              </p>
            </div>
          ) : (
            <ProductGrid products={data.items} />
          )}
        </div>
      </section>
    </main>
  );
}

export default ProductListingPage;
