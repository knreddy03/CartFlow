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
      className="border-y border-neutral-200 bg-[#f8f7f4]"
    >
      <div className="mx-auto flex max-w-[1600px] gap-8 overflow-x-auto px-5 py-4 sm:px-8 lg:px-12">
        {/* All */}
        <button
          type="button"
          onClick={() => onSelect(null)}
          className={`whitespace-nowrap text-xs font-medium uppercase tracking-[0.16em] transition-colors ${
            selectedSubCategoryId === null
              ? "text-neutral-950"
              : "text-neutral-500 hover:text-neutral-950"
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
            className={`whitespace-nowrap text-xs font-medium uppercase tracking-[0.16em] transition-colors ${
              selectedSubCategoryId === subCategory.id
                ? "text-neutral-950"
                : "text-neutral-500 hover:text-neutral-950"
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
