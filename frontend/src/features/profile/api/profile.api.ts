import { api } from "../../../api/axios";

import type { UserProfile } from "../profile.types";

export const getProfile = async () => {
  const response = await api.get<UserProfile>("/users/me");

  return response.data;
};
