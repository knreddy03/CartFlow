import { Link } from "react-router-dom";

import Loader from "../../../components/common/Loader";
import { useCategories } from "../../category/hooks/useCategories";
import type { Category } from "../../category/category.types";

function CategoryCard({ category }: { category: Category }) {
  return (
    <Link
      to={`/categories/${category.id}`}
      className="group relative block h-screen w-full snap-start overflow-hidden bg-neutral-100"
    >
      <img
        src={category.image_url}
        alt={category.name}
        className="absolute inset-0 h-full w-full object-cover transition-transform duration-[1800ms] ease-out group-hover:scale-[1.02]"
      />

      {/* Very subtle readability overlay */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/45 via-transparent to-transparent" />

      {/* Content */}
      <div className="absolute inset-x-0 bottom-0 z-10 px-6 pb-14 sm:px-10 sm:pb-16 lg:px-16 lg:pb-20">
        <div className="mx-auto max-w-[1600px] text-white">
          <p className="mb-3 text-xs font-medium uppercase tracking-[0.35em] text-white/80">
            Collection
          </p>

          <h2 className="text-6xl font-light tracking-[-0.04em] sm:text-7xl md:text-8xl lg:text-[9rem]">
            {category.name}
          </h2>

          {category.description && (
            <p className="mt-4 max-w-md text-sm leading-relaxed text-white/80 sm:text-base">
              {category.description}
            </p>
          )}
        </div>
      </div>
    </Link>
  );
}

function CategoryShowcase() {
  const { data: categories, isLoading, isError } = useCategories();

  if (isLoading) {
    return (
      <section className="flex h-screen items-center justify-center bg-neutral-950">
        <Loader />
      </section>
    );
  }

  if (isError) {
    return (
      <section className="flex h-screen items-center justify-center bg-neutral-950 px-5 text-center">
        <p className="text-sm text-neutral-400">Unable to load categories.</p>
      </section>
    );
  }

  if (!categories || categories.length === 0) {
    return null;
  }

  return (
    <main className="snap-y snap-mandatory">
      {categories.map((category) => (
        <CategoryCard key={category.id} category={category} />
      ))}
    </main>
  );
}

export default CategoryShowcase;
