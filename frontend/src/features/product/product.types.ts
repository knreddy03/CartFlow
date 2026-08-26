export interface Product {
  id: string;
  sub_category_id: string;
  name: string;
  slug: string;
  description: string | null;
  price: number;
  currency: string;
  stock_quantity: number;
  image_url: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProductListResponse {
  items: Product[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface ProductFilters {
  category_id?: string;
  sub_category_id?: string;
  is_active?: boolean;
  min_price?: number;
  max_price?: number;
  page?: number;
  page_size?: number;
}
