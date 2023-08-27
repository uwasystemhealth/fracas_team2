"use client";

import React, { Fragment, useState } from "react";
import {
  Box,
  Paper,
  TextField,
  Button,
  Checkbox,
  Link,
  Typography,
  FormControlLabel,
  Grid,
} from "@mui/material";
import LogoSVG from "../public/UWAM Logo 2023 (colour).svg";
import Image from "next/image";
import axios, { AxiosError, AxiosResponse } from "axios";
import { API_CLIENT, API_ENDPOINT } from "@/helpers/api";
import { useRouter } from "next/navigation";

interface AuthenticationSignupSend {
  token: string;
  password: string;
}

interface AuthenticationSignupResponse {
  err: string;
  msg: string;
}

const SignUpForm: React.FC = () => {
  const [confirmPassword, setConfirmPassword] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const router = useRouter();

  const handleConfirmPasswordChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setConfirmPassword(event.target.value);
  };

  const handlePasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(event.target.value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(password !== confirmPassword);
    if (password === confirmPassword) {
      const token = new URLSearchParams(window.location.search).get("token");
      try {
        const response = await API_CLIENT.post<
          AuthenticationSignupSend,
          AxiosResponse<AuthenticationSignupResponse>
        >(API_ENDPOINT.AUTHENTICATION.SIGNUP, {
          token: token,
          password: password,
        })
          .then((response) => {
            if (response) {
              const { err: err, msg: msg } = response.data;
              console.log(err, msg);
              console.log("User registered.");

              router.push("/login?new_user=1");
            } else {
              setErrorMessage("An error occurred");
            }
          })
          .catch((error: AxiosError<AuthenticationSignupResponse>) => {
            if (error.response) {
              const { err: err, msg: msg } = error.response.data;
              setErrorMessage(`An error occurred. Error code ${err} ${msg}`);
            } else {
              setErrorMessage("An error occurred");
            }
          });

        // Do something with the token (e.g., store it)
      } catch (error: any) {}
    }
  };

  return (
    <Paper
      elevation={3}
      style={{
        margin: 20,
        padding: 20,
        maxWidth: "75vw",
        alignItems: "center",
      }}
    >
      <Image
        src={LogoSVG}
        alt="Logo"
        width={446}
        height={91.6833}
        layout="responsive"
      />
      <Typography variant="h1" textAlign="center">
        Sign up
      </Typography>
      <Typography maxWidth={700}>
        Welcome to Better FRACAS! You have been invited by your team lead to
        join this organization. Please complete registration by setting your
        password.
      </Typography>
      <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
        <TextField
          value={password}
          onChange={handlePasswordChange}
          margin="normal"
          required
          fullWidth
          name="password"
          label="Password"
          type="password"
          id="password"
          autoComplete="current-password"
          helperText={
            error && (
              <Typography color="error">{"Passwords don't match."}</Typography>
            )
          }
          error={error}
          autoFocus
        />
        <TextField
          value={confirmPassword}
          onChange={handleConfirmPasswordChange}
          margin="normal"
          required
          fullWidth
          id="confirm-password"
          label="Confirm Password"
          name="confirm-password"
          type="password"
          helperText={
            error && (
              <Typography color="error">{"Passwords don't match."}</Typography>
            )
          }
          error={error}
        />
        <Button
          type="submit"
          fullWidth
          variant="contained"
          sx={{ mt: 3, mb: 2 }}
        >
          Sign In
        </Button>
        <Typography color="error">{errorMessage}</Typography>
      </Box>
    </Paper>
  );
};

export default SignUpForm;
