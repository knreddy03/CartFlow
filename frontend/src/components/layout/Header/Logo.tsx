import { Link } from "react-router-dom";

interface LogoProps {
  transparent?: boolean;
}

function Logo({ transparent = false }: LogoProps) {
  return (
    <Link
      to="/"
      className={`text-3xl font-bold ${
        transparent ? "text-white" : "text-black"
      }`}
    >
      CartFlow
    </Link>
  );
}

export default Logo;
