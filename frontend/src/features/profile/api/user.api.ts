import { api } from "./axios";

export const getCurrentUser = async () => {
  console.log("Calling GET /users/me");

  const response = await api.get("/users/me");

  console.log(response.data);

  return response.data;
};
