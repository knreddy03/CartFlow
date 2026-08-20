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
      className="group relative block min-h-[360px] overflow-hidden bg-neutral-200"
    >
      {subCategory.image_url ? (
        <img
          src={subCategory.image_url}
          alt={subCategory.name}
          className="absolute inset-0 h-full w-full object-cover transition-transform duration-700 ease-out group-hover:scale-105"
        />
      ) : (
        <div className="absolute inset-0 bg-neutral-200" />
      )}

      <div className="absolute inset-0 bg-gradient-to-t from-black/65 via-black/10 to-transparent" />

      <div className="absolute inset-x-0 bottom-0 p-6 text-white">
        <div className="flex items-end justify-between gap-4">
          <div>
            <p className="mb-2 text-xs uppercase tracking-[0.25em] text-white/70">
              Collection
            </p>

            <h3 className="text-3xl font-light tracking-tight">
              {subCategory.name}
            </h3>

            {subCategory.description && (
              <p className="mt-2 max-w-xs text-sm leading-relaxed text-white/75">
                {subCategory.description}
              </p>
            )}
          </div>

          <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/50 transition-all duration-300 group-hover:border-white group-hover:bg-white group-hover:text-neutral-950">
            <ArrowUpRight className="h-5 w-5 transition-transform duration-300 group-hover:rotate-45" />
          </span>
        </div>
      </div>
    </Link>
  );
}

export default SubCategoryCard;
