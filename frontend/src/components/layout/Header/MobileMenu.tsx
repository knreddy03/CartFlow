import { useEffect, useRef } from "react";
import type { RefObject } from "react";
import { X } from "lucide-react";
import { Link } from "react-router-dom";

import { useAuth } from "../../../features/auth/hooks/useAuth";
import { useCategories } from "../../../features/category/hooks/useCategories";

interface MobileMenuProps {
  open: boolean;
  onClose: () => void;
  triggerRef: RefObject<HTMLButtonElement | null>;
}

function MobileMenu({ open, onClose, triggerRef }: MobileMenuProps) {
  const { isAuthenticated, logout } = useAuth();
  const { data: categories = [], isLoading, isError } = useCategories();

  const hasOpenedRef = useRef(false);
  const closeButtonRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (!open) {
      document.body.style.overflow = "";

      if (hasOpenedRef.current) {
        triggerRef.current?.focus();
      }
      closeButtonRef.current?.focus();
      return;
    }

    hasOpenedRef.current = true;

    document.body.style.overflow = "hidden";

    requestAnimationFrame(() => {
      closeButtonRef.current?.focus();
    });

    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        onClose();
      }
    }

    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.body.style.overflow = "";
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [open, onClose, triggerRef]);

  if (!open) {
    return null;
  }

  function handleLogout() {
    logout();
    onClose();
  }

  return (
    <div
      id="mobile-navigation"
      role="dialog"
      aria-modal="true"
      aria-label="Mobile navigation"
      className="fixed inset-0 z-[60] bg-white lg:hidden"
    >
      {/* Header */}
      <div className="flex h-16 items-center justify-between border-b border-gray-200 px-5 sm:px-8">
        <Link
          to="/"
          onClick={onClose}
          className="text-lg font-semibold uppercase tracking-[0.2em] text-gray-900"
        >
          CartFlow
        </Link>

        <button
          ref={closeButtonRef}
          type="button"
          onClick={onClose}
          aria-label="Close menu"
          className="rounded-full p-2 text-gray-900 transition-colors hover:bg-gray-100"
        >
          <X className="h-5 w-5" />
        </button>
      </div>

      {/* Navigation */}
      <nav className="px-5 py-10 sm:px-8">
        <div className="flex flex-col">
          <Link
            to="/"
            onClick={onClose}
            className="flex items-center justify-between border-b border-gray-200 py-5 text-2xl font-light tracking-tight text-gray-900 transition-colors hover:text-gray-600"
          >
            <span>Home</span>
            <span className="text-xs text-gray-400">01</span>
          </Link>

          {!isLoading &&
            !isError &&
            categories
              .filter((category) => category.is_active)
              .map((category, index) => (
                <Link
                  key={category.id}
                  to={`/categories/${category.id}`}
                  onClick={onClose}
                  className="flex items-center justify-between border-b border-gray-200 py-5 text-2xl font-light tracking-tight text-gray-900 transition-colors hover:text-gray-600"
                >
                  <span>{category.name}</span>

                  <span className="text-xs text-gray-400">
                    {String(index + 2).padStart(2, "0")}
                  </span>
                </Link>
              ))}
        </div>

        {/* Account */}
        <div className="mt-10 border-t border-gray-200 pt-8">
          {isAuthenticated ? (
            <>
              <Link
                to="/profile"
                onClick={onClose}
                className="block py-3 text-sm uppercase tracking-[0.15em] text-gray-900 transition-colors hover:text-gray-600"
              >
                My Profile
              </Link>

              <button
                type="button"
                onClick={handleLogout}
                className="block py-3 text-sm uppercase tracking-[0.15em] text-gray-600 transition-colors hover:text-gray-900"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                onClick={onClose}
                className="block py-3 text-sm uppercase tracking-[0.15em] text-gray-900 transition-colors hover:text-gray-600"
              >
                Login
              </Link>

              <Link
                to="/register"
                onClick={onClose}
                className="block py-3 text-sm uppercase tracking-[0.15em] text-gray-600 transition-colors hover:text-gray-900"
              >
                Create Account
              </Link>
            </>
          )}
        </div>
      </nav>
    </div>
  );
}

export default MobileMenu;
