import { ArrowDownRight, ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";

import heroImage from "../../../assets/images/hero/hero.jpg";

function Hero() {
  return (
    <section className="group relative min-h-[calc(100vh-64px)] overflow-hidden bg-neutral-900">
      {/* Hero Image */}
      <img
        src={heroImage}
        alt="CartFlow new fashion collection"
        className="absolute inset-0 h-full w-full object-cover transition-transform duration-[2000ms] ease-out group-hover:scale-[1.02]"
      />

      {/* Editorial Overlay */}
      <div className="absolute inset-0 bg-black/35" />

      {/* Subtle Bottom Gradient */}
      <div className="absolute inset-x-0 bottom-0 h-1/2 bg-gradient-to-t from-black/50 to-transparent" />

      {/* Content */}
      <div className="relative z-10 mx-auto flex min-h-[calc(100vh-64px)] max-w-[1600px] items-center px-6 py-20 sm:px-10 lg:px-16">
        <div className="max-w-3xl text-white">
          {/* Eyebrow */}
          <div className="mb-8 flex items-center gap-4">
            <span className="h-px w-10 bg-white/70" />

            <p className="text-xs font-medium uppercase tracking-[0.35em] text-white/80">
              New Collection 2026
            </p>
          </div>

          {/* Heading */}
          <h1 className="max-w-3xl text-6xl font-light leading-[0.95] tracking-[-0.04em] sm:text-7xl md:text-8xl lg:text-[7rem]">
            The art of
            <br />
            <span className="font-normal italic">everyday style.</span>
          </h1>

          {/* Description */}
          <p className="mt-8 max-w-lg text-base leading-relaxed text-white/80 sm:text-lg">
            Curated pieces designed for effortless confidence, timeless
            silhouettes, and the way you live today.
          </p>

          {/* CTAs */}
          <div className="mt-10 flex flex-wrap items-center gap-6">
            <Link
              to="/products"
              className="group/button inline-flex items-center gap-3 bg-white px-7 py-4 text-sm font-medium uppercase tracking-[0.15em] text-neutral-950 transition-all duration-300 hover:bg-neutral-100"
            >
              <span>Shop Collection</span>

              <ArrowRight className="h-4 w-4 transition-transform duration-300 group-hover/button:translate-x-1" />
            </Link>

            <Link
              to="/sale"
              className="group/button inline-flex items-center gap-3 border-b border-white/70 pb-2 text-sm font-medium uppercase tracking-[0.15em] text-white transition-all duration-300 hover:border-white"
            >
              <span>Explore</span>

              <ArrowRight className="h-4 w-4 transition-transform duration-300 group-hover/button:translate-x-1" />
            </Link>
          </div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 right-6 z-10 hidden items-center gap-3 text-white/70 md:flex lg:right-16">
        <span className="text-[10px] uppercase tracking-[0.3em]">
          Scroll to explore
        </span>

        <ArrowDownRight className="h-4 w-4" />
      </div>

      {/* Collection Label */}
      <div className="absolute bottom-8 left-6 z-10 hidden text-xs uppercase tracking-[0.25em] text-white/60 md:block lg:left-16">
        CartFlow / 01
      </div>
    </section>
  );
}

export default Hero;
