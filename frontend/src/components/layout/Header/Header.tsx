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
      <header
        className={
          transparent
            ? "absolute inset-x-0 top-0 z-50 w-full"
            : "sticky top-0 z-50 w-full border-b border-neutral-200/80 bg-[#f8f7f4]/95 backdrop-blur-md"
        }
      >
        <div className="mx-auto flex h-16 max-w-[1600px] items-center justify-between px-5 sm:px-8 lg:px-12">
          {/* Mobile Menu */}
          <button
            ref={mobileMenuButtonRef}
            type="button"
            aria-label="Open menu"
            aria-expanded={mobileMenuOpen}
            aria-controls="mobile-navigation"
            onClick={() => setMobileMenuOpen(true)}
            className={`rounded-full p-2 transition-colors lg:hidden ${
              transparent
                ? "text-white hover:bg-white/10"
                : "text-neutral-900 hover:bg-neutral-100"
            }`}
          >
            <Menu className="h-5 w-5" />
          </button>

          {/* Logo */}
          <div className="shrink-0 lg:absolute lg:left-12">
            <Logo transparent={transparent} />
          </div>

          {/* Desktop Navigation */}
          <div className="mx-auto hidden lg:block">
            <NavLinks transparent={transparent} />
          </div>

          {/* Actions */}
          <div className="ml-auto flex items-center gap-1 sm:gap-2">
            <SearchButton transparent={transparent} />

            <WishlistButton transparent={transparent} />

            <div className="hidden lg:block">
              <ProfileMenu transparent={transparent} />
            </div>

            <CartButton transparent={transparent} />
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
