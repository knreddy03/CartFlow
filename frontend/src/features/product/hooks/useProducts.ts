import { useQuery } from "@tanstack/react-query";

import { getProducts } from "../api/product.api";
import type { ProductFilters } from "../product.types";

export function useProducts(filters: ProductFilters = {}) {
  return useQuery({
    queryKey: ["products", filters],
    queryFn: () => getProducts(filters),
  });
}
