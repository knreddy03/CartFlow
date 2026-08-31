import { useNavigate } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";

function LogoutButton() {
  const navigate = useNavigate();

  const { logout } = useAuth();

  const handleLogout = () => {
    logout();

    navigate("/login");
  };

  return (
    <button
      onClick={handleLogout}
      className="rounded-lg bg-red-600 px-4 py-2.5 text-sm font-semibold uppercase tracking-[0.08em] text-white transition-colors duration-200 hover:bg-red-700 active:bg-red-800 disabled:opacity-50"
    >
      Logout
    </button>
  );
}

export default LogoutButton;
