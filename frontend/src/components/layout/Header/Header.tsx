import { Menu } from "lucide-react";
import { useRef, useState } from "react";

import Logo from "./Logo";
import NavLinks from "./NavLinks";
import ProfileMenu from "./ProfileMenu";
import SearchButton from "./SearchButton";
import WishlistButton from "./WishlistButton";
import CartButton from "./CartButton";
import MobileMenu from "./MobileMenu";

interface HeaderProps {
  variant?: "transparent" | "solid";
}

function Header({ variant = "transparent" }: HeaderProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const mobileMenuButtonRef = useRef<HTMLButtonElement>(null);

  const transparent = variant === "transparent";

  return (
    <>
      <header className="fixed inset-x-0 top-0 z-50 w-full border-b border-gray-200 bg-white/95 shadow-sm backdrop-blur-md">
        <div className="mx-auto grid h-16 max-w-[1600px] grid-cols-[1fr_auto_1fr] items-center px-5 sm:px-8 lg:px-12">
          {/* Mobile Menu Button */}
          <div className="flex items-center lg:hidden">
            <button
              ref={mobileMenuButtonRef}
              type="button"
              aria-label="Open menu"
              aria-expanded={mobileMenuOpen}
              aria-controls="mobile-navigation"
              onClick={() => setMobileMenuOpen(true)}
              className="rounded-full p-2 text-gray-900 transition-colors hover:bg-gray-100"
            >
              <Menu className="h-5 w-5" />
            </button>
          </div>

          {/* Logo */}
          <div className="shrink-0 lg:justify-self-start">
            <Logo transparent={transparent} />
          </div>

          {/* Desktop Navigation */}
          <div className="hidden lg:block lg:justify-self-center">
            <NavLinks transparent={transparent} />
          </div>

          {/* Actions */}
          <div className="flex items-center justify-self-end gap-1 sm:gap-2">
            <SearchButton transparent={false} />

            <WishlistButton transparent={false} />

            <div className="hidden lg:block">
              <ProfileMenu transparent={false} />
            </div>

            <CartButton transparent={false} />
          </div>
        </div>
      </header>

      <MobileMenu
        open={mobileMenuOpen}
        onClose={() => setMobileMenuOpen(false)}
        triggerRef={mobileMenuButtonRef}
      />
    </>
  );
}

export default Header;
