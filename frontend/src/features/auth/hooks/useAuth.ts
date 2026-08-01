import {
  useAuthStore,
} from "../auth.store";


export function useAuth(){

  const {
    access_token,
    refresh_token,
    isAuthenticated,
    login,
    logout,
  } = useAuthStore();


  return {
    access_token,
    refresh_token,
    isAuthenticated,
    login,
    logout,
  };

}