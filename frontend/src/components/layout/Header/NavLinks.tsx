import { NavLink } from "react-router-dom";

interface NavLinksProps {
  transparent?: boolean;
}

const links = [
  { name: "Home", path: "/" },
  { name: "Men", path: "/men" },
  { name: "Women", path: "/women" },
  { name: "Kids", path: "/kids" },
  { name: "Sale", path: "/sale" },
];

function NavLinks({ transparent = false }: NavLinksProps) {
  return (
    <nav className="hidden gap-8 lg:flex">
      {links.map((link) => (
        <NavLink
          key={link.path}
          to={link.path}
          className={() =>
            transparent
              ? "font-medium text-white hover:text-gray-300"
              : "font-medium text-gray-700 hover:text-black"
          }
        >
          {link.name}
        </NavLink>
      ))}
    </nav>
  );
}

export default NavLinks;
