import axios from "axios";
import LoginfromChromeExtension from "../login-service/LoginfromChromeExtension"

const axiosInstance = axios.create({
  baseURL: "http://localhost:3000", // 기본 API URL
  timeout: 5000, // 요청 타임아웃
});

axiosInstance.interceptors.request.use(
  (config) => {
    const access_token = localStorage.getItem("access_token");
    const id_token = localStorage.getItem("id_token");
    if (access_token) {
      config.headers.accessToken = access_token;
      config.headers.idToken = id_token;
    }
    return config;
  }
);

axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401) {
      console.error("Unauthorized, refreshing token...");
      localStorage.clear();
      LoginfromChromeExtension();
      const access_token = localStorage.getItem("access_token");
      const id_token = localStorage.getItem("id_token");
      if (access_token) {
        originalRequest.headers.accessToken = access_token;
        originalRequest.headers.idToken = id_token;
        return axiosInstance(originalRequest);
      }
      else{
        return originalRequest
      }
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
