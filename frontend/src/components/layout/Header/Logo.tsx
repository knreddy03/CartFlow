import { Link } from "react-router-dom";

interface LogoProps {
  transparent?: boolean;
}

function Logo({ transparent = false }: LogoProps) {
  return (
    <Link
      to="/"
      aria-label="CartFlow home"
      className={`group inline-flex items-center text-base font-semibold uppercase tracking-[0.25em] transition-opacity duration-300 hover:opacity-75 sm:text-base ${
        transparent ? "text-white" : "text-gray-900"
      }`}
    >
      CartFlow
    </Link>
  );
}

export default Logo;
