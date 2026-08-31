import { Heart } from "lucide-react";

interface Props {
  transparent?: boolean;
}

function WishlistButton({ transparent = false }: Props) {
  return (
    <button
      type="button"
      aria-label="Wishlist"
      className={`group rounded-full p-2.5 transition-colors duration-300 ${
        transparent
          ? "text-white hover:bg-white/10"
          : "text-gray-700 hover:bg-gray-100"
      }`}
    >
      <Heart className="h-[18px] w-[18px] transition-transform duration-300 group-hover:scale-110" />
    </button>
  );
}

export default WishlistButton;
