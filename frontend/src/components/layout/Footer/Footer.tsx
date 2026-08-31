function Footer() {
  return (
    <footer className="border-t border-gray-200 bg-white/95 backdrop-blur-sm">
      <div className="mx-auto max-w-[1600px] px-5 py-10 sm:px-8 lg:px-12">
        <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
          <div className="space-y-2">
            <p className="text-base font-semibold uppercase tracking-[0.28em] text-gray-900">
              CartFlow
            </p>

            <p className="text-sm text-gray-600">
              Modern style. Effortless shopping.
            </p>
          </div>

          <p className="text-[10px] uppercase tracking-[0.18em] text-gray-500">
            © 2026 CartFlow. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
