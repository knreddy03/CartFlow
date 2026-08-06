import { ShoppingCart } from "lucide-react";

interface Props {
  transparent?: boolean;
}

function CartButton({ transparent = false }: Props) {
  return (
    <button className="relative rounded-full p-2 hover:bg-white/10">
      <ShoppingCart className={`h-5 w-5 ${transparent ? "text-white" : ""}`} />

      <span className="absolute -right-1 -top-1 flex h-5 w-5 items-center justify-center rounded-full bg-red-600 text-xs text-white">
        0
      </span>
    </button>
  );
}

export default CartButton;
