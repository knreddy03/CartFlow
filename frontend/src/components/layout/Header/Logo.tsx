import { Link } from "react-router-dom";

interface LogoProps {
  transparent?: boolean;
}

function Logo({ transparent = false }: LogoProps) {
  return (
    <Link
      to="/"
      aria-label="CartFlow home"
      className={`group inline-flex items-center text-xl font-semibold uppercase tracking-[0.18em] transition-opacity duration-300 hover:opacity-70 sm:text-2xl ${
        transparent ? "text-white" : "text-neutral-950"
      }`}
    >
      CartFlow
    </Link>
  );
}

export default Logo;
