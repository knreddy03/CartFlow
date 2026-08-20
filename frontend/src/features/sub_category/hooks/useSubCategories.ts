import { useQuery } from "@tanstack/react-query";

import { getSubCategoriesByCategory } from "../api/subCategory.api";

export function useSubCategories(categoryId: string) {
  return useQuery({
    queryKey: ["sub-categories", categoryId],
    queryFn: () => getSubCategoriesByCategory(categoryId),
    enabled: Boolean(categoryId),
  });
}
