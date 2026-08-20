import { NavLink } from "react-router-dom";

import type { SubCategory } from "../subCategory.types";

interface SubCategoryNavProps {
  subCategories: SubCategory[];
}

function SubCategoryNav({ subCategories }: SubCategoryNavProps) {
  const activeSubCategories = subCategories.filter(
    (subCategory) => subCategory.is_active,
  );

  if (activeSubCategories.length === 0) {
    return null;
  }

  return (
    <nav
      aria-label="Sub category navigation"
      className="border-y border-neutral-200 bg-[#f8f7f4]"
    >
      <div className="mx-auto flex max-w-[1600px] gap-8 overflow-x-auto px-5 py-4 sm:px-8 lg:px-12">
        {activeSubCategories.map((subCategory) => (
          <NavLink
            key={subCategory.id}
            to={`/sub-categories/${subCategory.id}`}
            className={({ isActive }) =>
              `whitespace-nowrap text-xs font-medium uppercase tracking-[0.16em] transition-colors ${
                isActive
                  ? "text-neutral-950"
                  : "text-neutral-500 hover:text-neutral-950"
              }`
            }
          >
            {subCategory.name}
          </NavLink>
        ))}
      </div>
    </nav>
  );
}

export default SubCategoryNav;
