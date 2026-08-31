import { NavLink } from "react-router-dom";

import { useCategories } from "../../../features/category/hooks/useCategories";

interface NavLinksProps {
  transparent?: boolean;
}

function NavLinks({ transparent = false }: NavLinksProps) {
  const { data: categories = [], isLoading, isError } = useCategories();

  const linkClass = (isActive: boolean) =>
    `relative py-2 text-xs font-semibold uppercase tracking-[0.15em] transition-colors duration-300 ${
      transparent
        ? "text-white/80 hover:text-white"
        : "text-gray-700 hover:text-gray-900"
    } ${isActive ? (transparent ? "text-white" : "text-gray-900") : ""}`;

  return (
    <nav aria-label="Main navigation" className="flex items-center gap-8">
      <NavLink to="/" className={({ isActive }) => linkClass(isActive)}>
        {({ isActive }) => (
          <>
            <span>Home</span>

            {isActive && (
              <span className="absolute -bottom-1.5 left-0 h-1 w-full bg-gray-900" />
            )}
          </>
        )}
      </NavLink>

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
                    <span className="absolute -bottom-1.5 left-0 h-1 w-full bg-gray-900" />
                  )}
                </>
              )}
            </NavLink>
          ))}
    </nav>
  );
}

export default NavLinks;
