import { Search, Heart, ShoppingCart } from "lucide-react";

import Logo from "../navbar/Logo";
import NavLinks from "../layout/NavLinks";
import ProfileMenu from "../navbar/ProfileMenu";

function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b bg-white">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        <Logo />

        <NavLinks />

        <div className="flex items-center gap-2">
          <button className="rounded-full p-2 hover:bg-gray-100">
            <Search className="h-5 w-5" />
          </button>

          <button className="rounded-full p-2 hover:bg-gray-100">
            <Heart className="h-5 w-5" />
          </button>

          <ProfileMenu />

          <button className="relative rounded-full p-2 hover:bg-gray-100">
            <ShoppingCart className="h-5 w-5" />

            <span className="absolute -right-1 -top-1 flex h-5 w-5 items-center justify-center rounded-full bg-black text-xs text-white">
              0
            </span>
          </button>
        </div>
      </div>
    </header>
  );
}

export default Navbar;
