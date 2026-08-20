import { api } from "../../../api/axios";

import type {
  Product,
  ProductFilters,
  ProductListResponse,
} from "../product.types";

export async function getProducts(
  filters: ProductFilters = {},
): Promise<ProductListResponse> {
  const response = await api.get<ProductListResponse>("/products", {
    params: filters,
  });

  return response.data;
}

export async function getProductById(productId: string): Promise<Product> {
  const response = await api.get<Product>(`/products/${productId}`);

  return response.data;
}
