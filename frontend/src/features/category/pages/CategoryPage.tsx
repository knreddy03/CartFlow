import { useParams } from "react-router-dom";

import { useCategories } from "../hooks/useCategories";
import { useSubCategories } from "../../sub_category/hooks/useSubCategories";
import SubCategoryCard from "../../sub_category/components/SubCategoryCard";
import SubCategoryNav from "../../sub_category/components/SubCategoryNav";

function CategoryPage() {
  const { categoryId } = useParams<{ categoryId: string }>();

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

  if (!categoryId) {
    return <p>Category not found.</p>;
  }

  if (categoriesLoading || subCategoriesLoading) {
    return (
      <main className="min-h-screen bg-[#f8f7f4] px-5 py-24 sm:px-8 lg:px-12">
        <div className="mx-auto max-w-[1600px]">
          <p className="text-sm text-neutral-500">Loading...</p>
        </div>
      </main>
    );
  }

  if (categoriesError || subCategoriesError) {
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
          <p className="mb-4 text-xs font-medium uppercase tracking-[0.3em] text-neutral-500">
            Collection
          </p>

          <h1 className="text-5xl font-light tracking-tight sm:text-6xl lg:text-7xl">
            {category.name}
          </h1>

          {category.description && (
            <p className="mt-5 max-w-xl text-sm leading-relaxed text-neutral-500">
              {category.description}
            </p>
          )}
        </div>
      </section>

      {/* Subcategory Navigation */}
      <SubCategoryNav subCategories={activeSubCategories} />

      {/* Subcategory Cards */}
      <section className="px-5 pb-24 pt-16 sm:px-8 lg:px-12 lg:pb-32">
        <div className="mx-auto max-w-[1600px]">
          <div className="mb-10">
            <p className="text-xs font-medium uppercase tracking-[0.3em] text-neutral-500">
              Explore
            </p>

            <h2 className="mt-3 text-3xl font-light tracking-tight sm:text-4xl">
              Shop by category
            </h2>
          </div>

          {activeSubCategories.length === 0 ? (
            <p className="text-sm text-neutral-500">
              No collections available.
            </p>
          ) : (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {activeSubCategories.map((subCategory) => (
                <SubCategoryCard
                  key={subCategory.id}
                  subCategory={subCategory}
                />
              ))}
            </div>
          )}
        </div>
      </section>
    </main>
  );
}

export default CategoryPage;
