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
          : "text-neutral-800 hover:bg-neutral-100"
      }`}
    >
      <Heart className="h-[18px] w-[18px] transition-transform duration-300 group-hover:scale-105" />
    </button>
  );
}

export default WishlistButton;
