import { NavLink } from "react-router-dom";

const links = [
  { name: "Home", path: "/" },
  { name: "Men", path: "/men" },
  { name: "Women", path: "/women" },
  { name: "Kids", path: "/kids" },
  { name: "Sale", path: "/sale" },
];

function NavLinks() {
  return (
    <nav className="hidden gap-8 md:flex">
      {links.map((link) => (
        <NavLink
          key={link.path}
          to={link.path}
          className={({ isActive }) =>
            isActive ? "font-semibold" : "text-gray-600 hover:text-black"
          }
        >
          {link.name}
        </NavLink>
      ))}
    </nav>
  );
}

export default NavLinks;
