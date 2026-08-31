import { api } from "../../../api/axios";

import type { UserProfile } from "../profile.types";

export const getCurrentUser = async (): Promise<UserProfile> => {
  const response = await api.get<UserProfile>("/users/me");

  return response.data;
};
