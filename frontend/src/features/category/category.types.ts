export interface Category {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  image_url: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}
