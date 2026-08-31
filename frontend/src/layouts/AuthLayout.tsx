import { Outlet } from "react-router-dom";

import Logo from "../components/layout/Header/Logo";

export default function AuthLayout() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 antialiased">
      <header className="border-b border-gray-200 bg-white/90 backdrop-blur-sm">
        <div className="mx-auto flex h-20 max-w-[1600px] items-center px-5 sm:px-8 lg:px-12">
          <Logo />
        </div>
      </header>

      <main
        className="flex min-h-[calc(100vh-5rem)] items-center justify-center px-4 py-12"
        role="main"
      >
        <div className="w-full max-w-md rounded-2xl border border-gray-200 bg-white p-8 shadow-[0_12px_40px_rgba(17,24,39,0.06)] ring-1 ring-gray-100">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
