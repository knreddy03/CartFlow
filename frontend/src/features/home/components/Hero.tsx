import { ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";

import heroImage from "../../../assets/images/hero/hero.jpg";

function Hero() {
  return (
    <section className="relative h-[calc(100vh-64px)] overflow-hidden">
      {/* Background Image */}
      <img
        src={heroImage}
        alt="Fashion Collection"
        className="absolute inset-0 h-full w-full object-cover"
      />

      {/* Dark Overlay */}
      <div className="absolute inset-0 bg-black/45" />

      {/* Content */}
      <div className="relative z-10 mx-auto flex h-full max-w-7xl items-center px-6">
        <div className="max-w-xl text-white">
          <p className="mb-4 text-sm font-semibold uppercase tracking-[0.35em] text-gray-200">
            New Collection 2026
          </p>

          <h1 className="mb-6 text-5xl font-bold leading-tight md:text-7xl">
            Discover
            <br />
            Your Style
          </h1>

          <p className="mb-8 text-lg text-gray-200">
            Premium fashion curated for every occasion. Discover timeless styles
            with effortless shopping.
          </p>

          <div className="flex flex-wrap gap-4">
            <Link
              to="/products"
              className="rounded-lg bg-white px-6 py-3 font-semibold text-black transition hover:bg-gray-100"
            >
              Shop Now
            </Link>

            <Link
              to="/sale"
              className="inline-flex items-center rounded-lg border border-white px-6 py-3 transition hover:bg-white hover:text-black"
            >
              Explore
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Hero;
