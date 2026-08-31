import { Link } from "react-router-dom";

import Loader from "../../../components/common/Loader";
import { useCategories } from "../../category/hooks/useCategories";
import type { Category } from "../../category/category.types";

function CategoryCard({ category }: { category: Category }) {
  return (
    <Link
      to={`/categories/${category.id}`}
      className="group relative block h-screen w-full snap-start overflow-hidden bg-gray-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-900 focus-visible:ring-inset"
      aria-label={`View ${category.name} collection`}
    >
      <img
        src={category.image_url}
        alt={category.name}
        className="absolute inset-0 h-full w-full object-cover transition-transform duration-[1800ms] ease-out group-hover:scale-[1.02]"
        loading="lazy"
      />

      {/* Very subtle readability overlay */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-black/20 to-transparent" />

      {/* Content */}
      <div className="absolute inset-x-0 bottom-0 z-10 px-6 pb-14 sm:px-10 sm:pb-16 lg:px-16 lg:pb-20 transition-all duration-700 ease-out group-hover:translate-y-0">
        <div className="mx-auto max-w-[1600px] text-white">
          <p className="mb-3 text-xs font-semibold uppercase tracking-[0.35em] text-white/75 transition-all duration-500 ease-out group-hover:text-white/90 group-hover:tracking-[0.45em]">
            Collection
          </p>

          <h2 className="text-6xl font-light tracking-[-0.04em] sm:text-7xl md:text-8xl lg:text-[9rem] transition-all duration-700 ease-out group-hover:text-white/95">
            {category.name}
          </h2>

          {category.description && (
            <p className="mt-4 max-w-md text-sm leading-relaxed text-white/70 sm:text-base transition-all duration-700 ease-out group-hover:text-white/85">
              {category.description}
            </p>
          )}
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute inset-x-0 bottom-6 z-20 flex items-center justify-center transition-opacity duration-500 ease-out group-hover:opacity-0">
        <div className="animate-bounce">
          <svg
            className="h-5 w-5 text-white/60"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 14l-7 7m0 0l-7-7m7 7V3"
            />
          </svg>
        </div>
      </div>
    </Link>
  );
}

function CategoryShowcase() {
  const { data: categories, isLoading, isError } = useCategories();

  if (isLoading) {
    return (
      <section
        className="flex h-screen items-center justify-center bg-gray-900"
        role="status"
        aria-live="polite"
      >
        <div className="flex flex-col items-center gap-6">
          <Loader size="lg" />
          <p className="text-sm text-gray-400 animate-pulse">
            Loading collections...
          </p>
        </div>
      </section>
    );
  }

  if (isError) {
    return (
      <section
        className="flex h-screen items-center justify-center bg-gray-900 px-5 text-center"
        role="alert"
      >
        <div className="space-y-4">
          <div>
            <p className="text-base font-semibold text-gray-300 mb-2">
              Unable to load collections
            </p>
            <p className="text-sm text-gray-500">
              Please try refreshing the page or contact support if the problem
              persists.
            </p>
          </div>
        </div>
      </section>
    );
  }

  if (!categories || categories.length === 0) {
    return (
      <section
        className="flex h-screen items-center justify-center bg-gray-900 px-5 text-center"
        role="status"
      >
        <p className="text-sm text-gray-500">
          No collections available at this time.
        </p>
      </section>
    );
  }

  return (
    <main className="snap-y snap-mandatory" role="main">
      {categories.map((category) => (
        <CategoryCard key={category.id} category={category} />
      ))}
    </main>
  );
}

export default CategoryShowcase;
