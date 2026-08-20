function Footer() {
  return (
    <footer className="border-t border-neutral-200 bg-[#f8f7f4]">
      <div className="mx-auto max-w-[1600px] px-5 py-10 sm:px-8 lg:px-12">
        <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
          {/* Brand */}
          <div>
            <p className="text-lg font-semibold uppercase tracking-[0.18em] text-neutral-950">
              CartFlow
            </p>

            <p className="mt-2 text-sm text-neutral-500">
              Modern style. Effortless shopping.
            </p>
          </div>

          {/* Copyright */}
          <p className="text-xs uppercase tracking-[0.12em] text-neutral-400">
            © 2026 CartFlow. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
