import * as React from "react";
import { Box } from "@mui/material";
import { Head } from "../Head";
import { useLocation } from "react-router";
import ResponsiveAppBar from "../AppBar/AppBar";

type Title = {
  name: string;
  navigateTo: string;
};

type MainLayoutProps = {
  children: React.ReactNode;
};

const pages = [{ name: "Home", navigateTo: "/home" }];

export const MainLayout = ({ children }: MainLayoutProps) => {
  const location = useLocation();
  const currentTitle = pages.find(
    (page) => page.navigateTo === location.pathname.split("/")[1]
  )?.name;

  return (
    <>
      <Head title={currentTitle} />
      <ResponsiveAppBar />
      <Box>{children}</Box>
    </>
  );
};
