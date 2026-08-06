import { Search } from "lucide-react";

interface Props {
  transparent?: boolean;
}

function SearchButton({ transparent = false }: Props) {
  return (
    <button className="rounded-full p-2 hover:bg-white/10">
      <Search className={`h-5 w-5 ${transparent ? "text-white" : ""}`} />
    </button>
  );
}

export default SearchButton;
