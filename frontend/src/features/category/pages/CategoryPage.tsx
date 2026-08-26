import { useState } from "react";
import { useParams } from "react-router-dom";

import { useCategories } from "../hooks/useCategories";
import { useSubCategories } from "../../sub_category/hooks/useSubCategories";
import SubCategoryNav from "../../sub_category/components/SubCategoryNav";

import { useProducts } from "../../product/hooks/useProducts";
import ProductGrid from "../../product/components/ProductGrid";

function CategoryPage() {
  const { categoryId } = useParams<{ categoryId: string }>();

  const [selectedSubCategoryId, setSelectedSubCategoryId] = useState<
    string | null
  >(null);

  const {
    data: categories = [],
    isLoading: categoriesLoading,
    isError: categoriesError,
  } = useCategories();

  const {
    data: subCategories = [],
    isLoading: subCategoriesLoading,
    isError: subCategoriesError,
  } = useSubCategories(categoryId ?? "");

  const {
    data: productsData,
    isLoading: productsLoading,
    isError: productsError,
  } = useProducts(
    selectedSubCategoryId
      ? {
          sub_category_id: selectedSubCategoryId,
          is_active: true,
        }
      : {
          category_id: categoryId,
          is_active: true,
        },
  );

  if (!categoryId) {
    return <p>Category not found.</p>;
  }

  if (categoriesLoading || subCategoriesLoading || productsLoading) {
    return (
      <main className="min-h-screen bg-[#f8f7f4] px-5 py-24 sm:px-8 lg:px-12">
        <div className="mx-auto max-w-[1600px]">
          <p className="text-sm text-neutral-500">Loading...</p>
        </div>
      </main>
    );
  }

  if (categoriesError || subCategoriesError || productsError) {
    return (
      <main className="min-h-screen bg-[#f8f7f4] px-5 py-24 sm:px-8 lg:px-12">
        <div className="mx-auto max-w-[1600px]">
          <p className="text-sm text-neutral-500">
            Unable to load this category.
          </p>
        </div>
      </main>
    );
  }

  const category = categories.find((item) => item.id === categoryId);

  if (!category) {
    return (
      <main className="min-h-screen bg-[#f8f7f4] px-5 py-24 sm:px-8 lg:px-12">
        <div className="mx-auto max-w-[1600px]">
          <h1 className="text-3xl font-light">Category not found.</h1>
        </div>
      </main>
    );
  }

  const activeSubCategories = subCategories.filter(
    (subCategory) => subCategory.is_active,
  );

  return (
    <main className="min-h-screen bg-[#f8f7f4]">
      {/* Category Header */}
      <section className="px-5 pb-10 pt-24 sm:px-8 lg:px-12 lg:pb-12 lg:pt-32">
        <div className="mx-auto max-w-[1600px]">
          <p className="text-xs font-medium uppercase tracking-[0.3em] text-neutral-500">
            Collection
          </p>

          <h1 className="mt-3 text-4xl font-light tracking-tight sm:text-5xl">
            {category.name}
          </h1>

          {category.description && (
            <p className="mt-4 max-w-2xl text-sm leading-relaxed text-neutral-500">
              {category.description}
            </p>
          )}
        </div>
      </section>

      {/* Product Filter Navigation */}
      <SubCategoryNav
        subCategories={activeSubCategories}
        selectedSubCategoryId={selectedSubCategoryId}
        onSelect={setSelectedSubCategoryId}
      />

      {/* Products */}
      <section className="px-5 pb-24 pt-16 sm:px-8 lg:px-12 lg:pb-32">
        <div className="mx-auto max-w-[1600px]">
          <div className="mb-10 flex items-end justify-between gap-4">
            <div>
              <p className="text-xs font-medium uppercase tracking-[0.3em] text-neutral-500">
                {selectedSubCategoryId ? "Collection" : category.name}
              </p>

              <h2 className="mt-3 text-3xl font-light tracking-tight sm:text-4xl">
                {selectedSubCategoryId
                  ? subCategories.find(
                      (subCategory) => subCategory.id === selectedSubCategoryId,
                    )?.name
                  : "All products"}
              </h2>
            </div>

            {productsData && (
              <p className="text-sm text-neutral-500">
                {productsData.total}{" "}
                {productsData.total === 1 ? "product" : "products"}
              </p>
            )}
          </div>

          <ProductGrid products={productsData?.items ?? []} />
        </div>
      </section>
    </main>
  );
}

export default CategoryPage;
