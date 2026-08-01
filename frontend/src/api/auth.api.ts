import { api } from "./axios";


export interface RegisterPayload {
  first_name: string;
  last_name: string;
  date_of_birth: string;
  mobile: string;
  email: string;
  password: string;
}


export interface RegisterResponse {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  mobile: string;
  date_of_birth: string;
}


export const registerUser = async (
  payload: RegisterPayload
) => {

  const response = await api.post<RegisterResponse>(
    "/auth/register",
    payload
  );

  return response.data;
};


export interface LoginPayload {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: "bearer";
}

export const loginUser = async (
  payload: LoginPayload
) => {
  const response = await api.post<LoginResponse>(
    "/auth/login",
    payload
  );

  return response.data;
};