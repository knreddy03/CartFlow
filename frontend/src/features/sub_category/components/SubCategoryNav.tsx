import type { SubCategory } from "../subCategory.types";

interface SubCategoryNavProps {
  subCategories: SubCategory[];
  selectedSubCategoryId: string | null;
  onSelect: (subCategoryId: string | null) => void;
}

function SubCategoryNav({
  subCategories,
  selectedSubCategoryId,
  onSelect,
}: SubCategoryNavProps) {
  const activeSubCategories = subCategories.filter(
    (subCategory) => subCategory.is_active,
  );

  return (
    <nav
      aria-label="Sub category navigation"
      className="sticky top-16 z-40 border-y border-gray-200 bg-white/95 backdrop-blur-md"
    >
      <div className="mx-auto flex max-w-[1600px] gap-8 overflow-x-auto px-5 py-4 sm:px-8 lg:px-12 scrollbar-hide">
        {/* All */}
        <button
          type="button"
          onClick={() => onSelect(null)}
          className={`relative whitespace-nowrap text-xs font-semibold uppercase tracking-[0.15em] transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-900 focus-visible:ring-offset-2 pb-2 ${
            selectedSubCategoryId === null
              ? "text-gray-900 after:absolute after:bottom-0 after:left-0 after:h-1 after:w-full after:bg-gray-900"
              : "text-gray-600 hover:text-gray-900 after:absolute after:bottom-0 after:left-0 after:h-1 after:w-0 after:bg-gray-900 after:transition-all after:duration-300 hover:after:w-full"
          }`}
        >
          All
        </button>

        {/* Subcategories */}
        {activeSubCategories.map((subCategory) => (
          <button
            key={subCategory.id}
            type="button"
            onClick={() => onSelect(subCategory.id)}
            className={`relative whitespace-nowrap text-xs font-semibold uppercase tracking-[0.15em] transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-900 focus-visible:ring-offset-2 pb-2 ${
              selectedSubCategoryId === subCategory.id
                ? "text-gray-900 after:absolute after:bottom-0 after:left-0 after:h-1 after:w-full after:bg-gray-900"
                : "text-gray-600 hover:text-gray-900 after:absolute after:bottom-0 after:left-0 after:h-1 after:w-0 after:bg-gray-900 after:transition-all after:duration-300 hover:after:w-full"
            }`}
          >
            {subCategory.name}
          </button>
        ))}
      </div>
    </nav>
  );
}

export default SubCategoryNav;
