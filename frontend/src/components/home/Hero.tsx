import { ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";

function Hero() {
  return (
    <section className="relative h-[80vh] overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-r from-gray-900 via-gray-800 to-gray-700" />

      {/* Overlay */}
      <div className="absolute inset-0 bg-black/40" />

      {/* Content */}
      <div className="relative z-10 mx-auto flex h-full max-w-7xl items-center px-8">
        <div className="max-w-2xl text-white">
          <p className="mb-4 text-sm uppercase tracking-[0.4em]">
            New Collection 2026
          </p>

          <h1 className="mb-6 text-6xl font-bold leading-tight">
            Discover
            <br />
            Your Style
          </h1>

          <p className="mb-8 text-lg text-gray-300">
            Shop premium fashion with fast delivery, secure checkout, and
            effortless returns.
          </p>

          <div className="flex gap-4">
            <Link
              to="/products"
              className="rounded-lg bg-white px-8 py-4 font-semibold text-black transition hover:scale-105"
            >
              Shop Now
            </Link>

            <Link
              to="/sale"
              className="flex items-center rounded-lg border border-white px-8 py-4"
            >
              Explore
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Hero;
