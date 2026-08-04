import { useEffect, useRef, useState } from "react";
import { User } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../../features/auth/hooks/useAuth";

function ProfileMenu() {
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
        onClick={() => setOpen(!open)}
        className="rounded-full p-2 hover:bg-gray-100"
      >
        <User className="h-5 w-5" />
      </button>

      {open && (
        <div className="absolute right-0 mt-2 w-48 rounded-lg border bg-white shadow-lg">
          {!isAuthenticated ? (
            <>
              <Link
                to="/login"
                onClick={() => setOpen(false)}
                className="block px-4 py-3 hover:bg-gray-100"
              >
                Login
              </Link>

              <Link
                to="/register"
                onClick={() => setOpen(false)}
                className="block px-4 py-3 hover:bg-gray-100"
              >
                Register
              </Link>
            </>
          ) : (
            <>
              <Link
                to="/profile"
                onClick={() => setOpen(false)}
                className="block px-4 py-3 hover:bg-gray-100"
              >
                My Profile
              </Link>

              <button
                onClick={handleLogout}
                className="w-full px-4 py-3 text-left hover:bg-gray-100"
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
