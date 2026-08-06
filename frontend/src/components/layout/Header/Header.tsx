import Logo from "./Logo";
import NavLinks from "./NavLinks";
import ProfileMenu from "./ProfileMenu";
import SearchButton from "./SearchButton";
import WishlistButton from "./WishlistButton";
import CartButton from "./CartButton";

interface HeaderProps {
  variant?: "transparent" | "solid";
}

function Header({ variant = "solid" }: HeaderProps) {
  const transparent = variant === "transparent";

  return (
    <header
      className={
        transparent
          ? "absolute top-0 left-0 z-50 w-full"
          : "sticky top-0 z-50 border-b bg-white shadow-sm"
      }
    >
      <div className="mx-auto flex h-20 max-w-7xl items-center justify-between px-8">
        <Logo transparent={transparent} />

        <NavLinks transparent={transparent} />

        <div className="flex items-center gap-3">
          <SearchButton transparent={transparent} />

          <WishlistButton transparent={transparent} />

          <ProfileMenu transparent={transparent} />

          <CartButton transparent={transparent} />
        </div>
      </div>
    </header>
  );
}

export default Header;
