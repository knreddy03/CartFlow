import { useState } from "react";
import { useParams } from "react-router-dom";

import { useCategories } from "../hooks/useCategories";
import { useSubCategories } from "../../sub_category/hooks/useSubCategories";
import SubCategoryNav from "../../sub_category/components/SubCategoryNav";

import { useProducts } from "../../product/hooks/useProducts";
import ProductGrid from "../../product/components/ProductGrid";

function CategoryPage() {
  const { categoryId } = useParams<{ categoryId: string }>();

  const [selectedSubCategoryByCategory, setSelectedSubCategoryByCategory] =
    useState<Record<string, string | null>>({});

  const selectedSubCategoryId = categoryId
    ? (selectedSubCategoryByCategory[categoryId] ?? null)
    : null;

  const handleSelectSubCategory = (subCategoryId: string | null) => {
    if (!categoryId) {
      return;
    }

    setSelectedSubCategoryByCategory((previous) => ({
      ...previous,
      [categoryId]: subCategoryId,
    }));
  };

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
      <main className="min-h-screen bg-white px-5 py-24 sm:px-8 lg:px-12">
        <div className="mx-auto max-w-[1600px]">
          <p className="text-sm text-gray-400">Loading...</p>
        </div>
      </main>
    );
  }

  if (categoriesError || subCategoriesError || productsError) {
    return (
      <main className="min-h-screen bg-white px-5 py-24 sm:px-8 lg:px-12">
        <div className="mx-auto max-w-[1600px]">
          <p className="text-sm text-gray-400">Unable to load this category.</p>
        </div>
      </main>
    );
  }

  const category = categories.find((item) => item.id === categoryId);

  if (!category) {
    return (
      <main className="min-h-screen bg-white px-5 py-24 sm:px-8 lg:px-12">
        <div className="mx-auto max-w-[1600px]">
          <h1 className="text-3xl font-light text-gray-900">
            Category not found.
          </h1>
        </div>
      </main>
    );
  }

  const activeSubCategories = subCategories.filter(
    (subCategory) => subCategory.is_active,
  );

  return (
    <main className="min-h-screen bg-white">
      {/* Product Filter Navigation */}
      <SubCategoryNav
        subCategories={activeSubCategories}
        selectedSubCategoryId={selectedSubCategoryId}
        onSelect={handleSelectSubCategory}
      />

      {/* Products */}
      <section className="px-5 pb-32 pt-20 sm:px-8 lg:px-12 lg:pb-40">
        <div className="mx-auto max-w-[1600px]">
          <div className="mb-16 flex items-end justify-between gap-4">
            <div className="flex-1">
              <p className="text-xs font-semibold uppercase tracking-[0.4em] text-gray-500">
                {selectedSubCategoryId ? "Collection" : category.name}
              </p>

              <h2 className="mt-4 text-4xl font-light tracking-tight text-gray-900 sm:text-5xl">
                {selectedSubCategoryId
                  ? subCategories.find(
                      (subCategory) => subCategory.id === selectedSubCategoryId,
                    )?.name
                  : "All products"}
              </h2>
            </div>

            {productsData && (
              <p className="whitespace-nowrap text-base font-light text-gray-600">
                {productsData.total}{" "}
                <span className="text-gray-400">
                  {productsData.total === 1 ? "product" : "products"}
                </span>
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
