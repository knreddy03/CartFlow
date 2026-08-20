import { useQuery } from "@tanstack/react-query";

import { getProductById } from "../api/product.api";

export function useProduct(productId: string) {
  return useQuery({
    queryKey: ["product", productId],
    queryFn: () => getProductById(productId),
    enabled: Boolean(productId),
  });
}
