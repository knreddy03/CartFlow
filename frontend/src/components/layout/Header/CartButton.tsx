import { ShoppingBag } from "lucide-react";

interface Props {
  transparent?: boolean;
}

function CartButton({ transparent = false }: Props) {
  const itemCount = 0;

  return (
    <button
      type="button"
      aria-label={`Shopping bag${itemCount > 0 ? `, ${itemCount} items` : ""}`}
      className={`group relative rounded-full p-2.5 transition-colors duration-300 ${
        transparent
          ? "text-white hover:bg-white/10"
          : "text-gray-700 hover:bg-gray-100"
      }`}
    >
      <ShoppingBag className="h-[18px] w-[18px] transition-transform duration-300 group-hover:scale-110" />

      {itemCount > 0 && (
        <span className="absolute -right-0.5 -top-0.5 flex h-4 min-w-4 items-center justify-center rounded-full bg-gray-900 px-1 text-[9px] font-medium text-white">
          {itemCount}
        </span>
      )}
    </button>
  );
}

export default CartButton;
