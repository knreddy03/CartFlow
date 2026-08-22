import { NavLink } from "react-router-dom";

import { useCategories } from "../../../features/category/hooks/useCategories";

interface NavLinksProps {
  transparent?: boolean;
}

function NavLinks({ transparent = false }: NavLinksProps) {
  const { data: categories = [], isLoading, isError } = useCategories();

  const linkClass = (isActive: boolean) =>
    `relative py-2 text-xs font-medium uppercase tracking-[0.16em] transition-colors duration-300 ${
      transparent
        ? "text-white/85 hover:text-white"
        : "text-neutral-600 hover:text-neutral-950"
    } ${isActive ? (transparent ? "text-white" : "text-neutral-950") : ""}`;

  return (
    <nav aria-label="Main navigation" className="flex items-center gap-8">
      {/* Home */}
      <NavLink to="/" className={({ isActive }) => linkClass(isActive)}>
        {({ isActive }) => (
          <>
            <span>Home</span>

            {isActive && (
              <span className="absolute -bottom-1 left-0 h-px w-full bg-current" />
            )}
          </>
        )}
      </NavLink>

      {/* Categories */}
      {!isLoading &&
        !isError &&
        categories
          .filter((category) => category.is_active)
          .map((category) => (
            <NavLink
              key={category.id}
              to={`/categories/${category.id}`}
              className={({ isActive }) => linkClass(isActive)}
            >
              {({ isActive }) => (
                <>
                  <span>{category.name}</span>

                  {isActive && (
                    <span className="absolute -bottom-1 left-0 h-px w-full bg-current" />
                  )}
                </>
              )}
            </NavLink>
          ))}
    </nav>
  );
}

export default NavLinks;
