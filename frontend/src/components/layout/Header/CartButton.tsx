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
          : "text-neutral-800 hover:bg-neutral-100"
      }`}
    >
      <ShoppingBag className="h-[18px] w-[18px] transition-transform duration-300 group-hover:scale-105" />

      {itemCount > 0 && (
        <span className="absolute -right-0.5 -top-0.5 flex h-4 min-w-4 items-center justify-center rounded-full bg-neutral-950 px-1 text-[9px] font-medium text-white">
          {itemCount}
        </span>
      )}
    </button>
  );
}

export default CartButton;
