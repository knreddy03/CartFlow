import { Search } from "lucide-react";

interface Props {
  transparent?: boolean;
}

function SearchButton({ transparent = false }: Props) {
  return (
    <button
      type="button"
      aria-label="Search"
      className={`group rounded-full p-2.5 transition-colors duration-300 ${
        transparent
          ? "text-white hover:bg-white/10"
          : "text-gray-700 hover:bg-gray-100"
      }`}
    >
      <Search className="h-[18px] w-[18px] transition-transform duration-300 group-hover:scale-110" />
    </button>
  );
}

export default SearchButton;
