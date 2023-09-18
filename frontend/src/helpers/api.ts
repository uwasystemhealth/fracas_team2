import axios, { AxiosRequestConfig, AxiosResponse } from "axios";
import { BACKEND_URL } from "./constants";
import { string } from "prop-types";

export const API_ENDPOINT = {
  AUTHENTICATION: {
    LOGIN: "/api/v1/authentication/login",
    SIGNUP_REQUEST: "/api/v1/authentication/signup_request",
    SIGNUP: "/api/v1/authentication/signup",
    REFRESH: "/api/v1/authentication/refresh",
    LOGOUT: "/api/v1/authentication/logout",
    TEST_LOGGED_IN: "/api/v1/authentication/test_logged_in",
  },
  RECORD: "/api/v1/record",
  SUBSYSTEM: "/api/v1/subsystem",
};

export namespace API_TYPES {
  export interface NULLREQUEST_ {}
  export namespace AUTHENTICATION {
    export namespace LOGIN {
      export interface REQUEST {
        email: string;
        password: string;
      }
      export interface RESPONSE {
        access_token: string;
        refresh_token: string;
      }
    }
    export namespace SIGNUP {
      export interface REQUEST {
        token: string;
        password: string;
      }
      export interface RESPONSE {
        err: string;
        msg: string;
      }
    }
    export namespace TEST_LOGGED_IN {
      export interface RESPONSE {
        msg: string;
        email: string;
      }
    }
  }

  export namespace REPORT {
    export namespace POST {
      export interface RESPONSE {
        err: string;
        msg: string;
        id: number;
      }
    }
    export namespace PATCH {
      export interface REQUEST {
        title: string;
        subsystem_id: number;
        description: string;
        impact: string;
        cause: string;
        mechanism: string;
        corrective_action_plan: string;
        time_of_failure: string;
        car_year: string;
        creator_id: number;
        creator: string;
      }
      export interface RESPONSE {
        msg: string;
        err: string;
      }
    }
    export namespace DELETE {
      export interface RESPONSE {
        msg: string;
        err: string;
      }
    }
    export namespace GET {
      export interface RESPONSE {
        title: string;
        subsystem_id: number;
        description: string;
        impact: string;
        cause: string;
        mechanism: string;
        corrective_action_plan: string;
        time_of_failure: string;
        car_year: string;
        creator_id: number;
        creator: string;
      }
    }
  }
  export namespace SUBSYSTEM {
    export namespace POST {
      export interface REQUEST {
        subsystem: string;
      }
      export interface RESPONSE {
        id: number;
      }
    }
    export namespace GET {
      export interface RESPONSE {
        id: number;
        subsystem: string;
      }
    }
  }
}

export const TOKEN = {
  ACCESS: "access-token",
  REFRESH: "refresh-token",
};

export const AXIOS_CONFIG: AxiosRequestConfig = {
  baseURL: BACKEND_URL,
  timeout: 30000,
};

export const API_CLIENT = axios.create(AXIOS_CONFIG);

API_CLIENT.interceptors.request.use((config) => {
  const access_token = localStorage.getItem(TOKEN.ACCESS);
  config.headers.Authorization = access_token ? `Bearer ${access_token}` : "";
  return config;
});

// refresh tokens
API_CLIENT.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Check if the error is due to expired token
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      if (originalRequest.url === API_ENDPOINT.AUTHENTICATION.REFRESH) {
        console.error("Failed to refresh token");
        return;
      }

      try {
        // Refresh the access token
        const response = await axios.post(
          `${BACKEND_URL}${API_ENDPOINT.AUTHENTICATION.REFRESH}`,
          {},
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem(TOKEN.REFRESH)}`,
            },
          }
        );

        const newAccessToken = response.data.access_token;
        localStorage.setItem(TOKEN.ACCESS, newAccessToken);

        // Update the authorization header and retry the original request
        //  TODO: chekc
        API_CLIENT.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${newAccessToken}`;
        originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;
        return API_CLIENT(originalRequest);
      } catch (refreshError) {
        // Handle refresh error, e.g., redirect to login page
        console.error("Failed to refresh token", refreshError);
        // You might want to handle refresh error according to your app's logic
      }
    }

    return Promise.reject(error);
  }
);
