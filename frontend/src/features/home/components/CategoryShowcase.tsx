import { ArrowUpRight } from "lucide-react";
import { Link } from "react-router-dom";

import Loader from "../../../components/common/Loader";
import { useCategories } from "../../category/hooks/useCategories";
import type { Category } from "../../category/category.types";

function CategoryCard({ category }: { category: Category }) {
  return (
    <Link
      to={`/categories/${category.id}`}
      className="group relative block min-h-[480px] overflow-hidden bg-neutral-200 sm:min-h-[560px]"
    >
      <img
        src={category.image_url}
        alt={category.name}
        className="absolute inset-0 h-full w-full object-cover transition-transform duration-700 ease-out group-hover:scale-105"
      />

      <div className="absolute inset-0 bg-gradient-to-t from-black/65 via-black/10 to-transparent" />

      <div className="absolute inset-x-0 bottom-0 p-7 text-white sm:p-9">
        <div className="flex items-end justify-between gap-6">
          <div>
            <p className="mb-3 text-xs uppercase tracking-[0.25em] text-white/70">
              Collection
            </p>

            <h3 className="text-4xl font-light tracking-tight sm:text-5xl">
              {category.name}
            </h3>

            {category.description && (
              <p className="mt-3 max-w-xs text-sm leading-relaxed text-white/75">
                {category.description}
              </p>
            )}
          </div>

          <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full border border-white/50 transition-all duration-300 group-hover:border-white group-hover:bg-white group-hover:text-neutral-950">
            <ArrowUpRight className="h-5 w-5 transition-transform duration-300 group-hover:rotate-45" />
          </span>
        </div>
      </div>
    </Link>
  );
}

function CategoryShowcase() {
  const { data: categories, isLoading, isError } = useCategories();

  if (isLoading) {
    return (
      <section className="flex min-h-[400px] items-center justify-center bg-[#f8f7f4]">
        <Loader />
      </section>
    );
  }

  if (isError) {
    return (
      <section className="bg-[#f8f7f4] px-5 py-24 text-center">
        <p className="text-sm text-neutral-500">Unable to load categories.</p>
      </section>
    );
  }

  if (!categories || categories.length === 0) {
    return null;
  }

  return (
    <section className="bg-[#f8f7f4] px-5 py-24 sm:px-8 lg:px-12 lg:py-32">
      <div className="mx-auto max-w-[1600px]">
        <div className="mb-12 flex flex-col justify-between gap-5 md:mb-16 md:flex-row md:items-end">
          <div>
            <p className="mb-4 text-xs font-medium uppercase tracking-[0.3em] text-neutral-500">
              Explore
            </p>

            <h2 className="max-w-xl text-4xl font-light tracking-tight sm:text-5xl lg:text-6xl">
              Find your
              <span className="italic"> style.</span>
            </h2>
          </div>

          <p className="max-w-sm text-sm leading-relaxed text-neutral-500">
            Explore carefully curated collections designed to bring effortless
            style into every part of your wardrobe.
          </p>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          {categories.slice(0, 2).map((category) => (
            <CategoryCard key={category.id} category={category} />
          ))}

          {categories.length >= 3 && (
            <div className="md:col-span-2">
              <CategoryCard category={categories[2]} />
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

export default CategoryShowcase;
