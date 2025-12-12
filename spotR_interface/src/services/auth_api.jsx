import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000",
  withCredentials: true,
});

export const getCurrentUser = () => api.get("/api/me");
export const loginWithSpotify = () => {
  window.location.href = "http://127.0.0.1:5000/auth/spotify/login";
};
export const logout = () => api.post("/auth/spotify/logout");

export default api;
