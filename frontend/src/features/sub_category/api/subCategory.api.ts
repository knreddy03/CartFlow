import { api } from "../../../api/axios";
import type { SubCategory } from "../subCategory.types";

export async function getSubCategoriesByCategory(
  categoryId: string,
): Promise<SubCategory[]> {
  const response = await api.get<SubCategory[]>(
    `/sub-categories/category/${categoryId}`,
  );

  return response.data;
}
