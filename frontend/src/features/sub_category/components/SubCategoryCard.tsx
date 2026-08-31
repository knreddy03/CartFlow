import { ArrowUpRight } from "lucide-react";
import { Link } from "react-router-dom";

import type { SubCategory } from "../subCategory.types";

interface SubCategoryCardProps {
  subCategory: SubCategory;
}

function SubCategoryCard({ subCategory }: SubCategoryCardProps) {
  return (
    <Link
      to={`/sub-categories/${subCategory.id}`}
      className="group relative block min-h-[360px] overflow-hidden bg-gray-200 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-900 focus-visible:ring-offset-2 transition-transform duration-300 hover:shadow-xl"
      aria-label={`View ${subCategory.name} collection`}
    >
      {subCategory.image_url ? (
        <img
          src={subCategory.image_url}
          alt={subCategory.name}
          className="absolute inset-0 h-full w-full object-cover transition-transform duration-700 ease-out group-hover:scale-105"
          loading="lazy"
        />
      ) : (
        <div className="absolute inset-0 bg-gradient-to-br from-gray-300 to-gray-200" />
      )}

      <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent transition-all duration-500 ease-out group-hover:from-black/75" />

      <div className="absolute inset-x-0 bottom-0 p-6 text-white transition-all duration-500 ease-out">
        <div className="flex items-end justify-between gap-4">
          <div className="flex-1 space-y-1">
            <p className="text-xs uppercase tracking-[0.25em] text-white/70 font-semibold transition-all duration-500 ease-out group-hover:text-white/90 group-hover:tracking-[0.35em]">
              Collection
            </p>

            <h3 className="text-3xl font-light tracking-tight transition-all duration-500 ease-out group-hover:text-white/95">
              {subCategory.name}
            </h3>

            {subCategory.description && (
              <p className="mt-2 max-w-xs text-sm leading-relaxed text-white/70 transition-all duration-500 ease-out group-hover:text-white/85">
                {subCategory.description}
              </p>
            )}
          </div>

          <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/50 transition-all duration-300 group-hover:border-white group-hover:bg-white group-hover:text-gray-900 group-hover:shadow-lg">
            <ArrowUpRight className="h-5 w-5 transition-transform duration-300 group-hover:rotate-45" />
          </span>
        </div>
      </div>
    </Link>
  );
}

export default SubCategoryCard;
