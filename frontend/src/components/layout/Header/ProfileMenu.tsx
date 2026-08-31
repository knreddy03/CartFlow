import { useEffect, useRef, useState } from "react";
import { User } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../../../features/auth/hooks/useAuth";

interface ProfileMenuProps {
  transparent?: boolean;
}

function ProfileMenu({ transparent = false }: ProfileMenuProps) {
  const [open, setOpen] = useState(false);

  const menuRef = useRef<HTMLDivElement>(null);

  const navigate = useNavigate();

  const { isAuthenticated, logout } = useAuth();

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);

    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  function handleLogout() {
    logout();
    navigate("/");
    setOpen(false);
  }

  return (
    <div ref={menuRef} className="relative">
      <button
        type="button"
        aria-label="Account"
        aria-expanded={open}
        onClick={() => setOpen((current) => !current)}
        className={`group rounded-full p-2.5 transition-colors duration-300 ${
          transparent
            ? "text-white hover:bg-white/10"
            : "text-gray-700 hover:bg-gray-100"
        }`}
      >
        <User className="h-[18px] w-[18px] transition-transform duration-300 group-hover:scale-110" />
      </button>

      {open && (
        <div className="absolute right-0 top-full mt-3 w-52 border border-gray-200 bg-white p-2 shadow-lg">
          {!isAuthenticated ? (
            <>
              <Link
                to="/login"
                onClick={() => setOpen(false)}
                className="block px-4 py-3 text-sm text-gray-900 transition-colors hover:bg-gray-50"
              >
                Login
              </Link>

              <Link
                to="/register"
                onClick={() => setOpen(false)}
                className="block px-4 py-3 text-sm text-gray-900 transition-colors hover:bg-gray-50"
              >
                Create Account
              </Link>
            </>
          ) : (
            <>
              <Link
                to="/profile"
                onClick={() => setOpen(false)}
                className="block px-4 py-3 text-sm text-gray-900 transition-colors hover:bg-gray-50"
              >
                My Profile
              </Link>

              <button
                type="button"
                onClick={handleLogout}
                className="w-full px-4 py-3 text-left text-sm text-gray-900 transition-colors hover:bg-gray-50"
              >
                Logout
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default ProfileMenu;
