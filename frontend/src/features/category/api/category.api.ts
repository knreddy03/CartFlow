import { api } from "../../../api/axios";
import type { Category } from "../category.types";

export async function getCategories(): Promise<Category[]> {
  const response = await api.get<Category[]>("/categories");

  return response.data;
}
