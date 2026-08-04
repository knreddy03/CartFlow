import { useAuthStore } from "../auth.store";

export const useAuth = () => {
  const { isAuthenticated, access_token, refresh_token, login, logout } =
    useAuthStore();

  return {
    isAuthenticated,
    access_token,
    refresh_token,
    login,
    logout,
  };
};
