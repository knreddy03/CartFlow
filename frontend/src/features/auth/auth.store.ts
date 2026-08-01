import { create } from "zustand";
import { persist } from "zustand/middleware";

interface AuthState {
  access_token: string | null;
  refresh_token: string | null;
  token_type: string | null;

  isAuthenticated: boolean;

  login: (
    access_token: string,
    refresh_token: string,
    token_type: string,
  ) => void;

  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      access_token: null,
      refresh_token: null,
      token_type: null,

      isAuthenticated: false,

      login: (access_token, refresh_token, token_type) => {
        console.log("ZUSTAND LOGIN CALLED");

        set({
          access_token,

          refresh_token,

          token_type,

          isAuthenticated: true,
        });
      },

      logout: () => {
        set({
          access_token: null,
          refresh_token: null,
          token_type: null,
          isAuthenticated: false,
        });
      },
    }),

    {
      name: "cartflow-auth",
    },
  ),
);
