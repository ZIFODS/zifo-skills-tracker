import * as React from "react";
import { Box } from "@mui/material";
import { Head } from "../Head";
import { useLocation } from "react-router";

type Title = {
  name: string;
  navigateTo: string;
};

type MainLayoutProps = {
  children: React.ReactNode;
  header: any;
};

const pages = [{ name: "Home", navigateTo: "/home" }];

export const MainLayout = ({ children, header }: MainLayoutProps) => {
  const location = useLocation();
  const currentTitle = pages.find(
    (page) => page.navigateTo === location.pathname.split("/")[1]
  )?.name;

  return (
    <>
      <Head title={currentTitle} />
      <Box sx={{ px: 3 }}>{children}</Box>
    </>
  );
};
