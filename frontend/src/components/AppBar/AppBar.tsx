import * as React from "react";
import {
  AppBar,
  Box,
  Toolbar,
  IconButton,
  Typography,
  Menu,
  Avatar,
  Tooltip,
  MenuItem,
  Button,
  Stack,
} from "@mui/material";
import { useAuth } from "../../lib/auth";
import { useNavigate } from "react-router";
import zifoLogoImage from "../../assets/zifo-logo.png";

function ResponsiveAppBar() {
  const navigate = useNavigate();

  const [anchorElNav, setAnchorElNav] = React.useState<null | HTMLElement>(
    null
  );
  const [anchorElUser, setAnchorElUser] = React.useState<null | HTMLElement>(
    null
  );

  const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElNav(event.currentTarget);
  };
  const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  const { logout, user } = useAuth();

  const graphOnClick = () => {
    navigate("/graph");
  };

  const updateOnClick = () => {
    navigate("/update");
  };

  const adminOnClick = () => {
    navigate("/admin");
  };

  const pages = [
    {
      name: "Graph",
      onClick: graphOnClick,
    },
    {
      name: "Update",
      onClick: updateOnClick,
    },
    {
      name: "Admin",
      onClick: adminOnClick,
    },
  ];

  const settingOnClick = () => {
    navigate("/settings");
  };

  const settings = [
    {
      name: "Settings",
      onClick: settingOnClick,
    },
    {
      name: "Logout",
      onClick: logout,
    },
  ];

  return (
    <AppBar position="static" elevation={0} color="transparent">
      <Toolbar disableGutters sx={{ mx: 8 }}>
        <Box
          component="img"
          sx={{ width: 50, height: 23, mr: 4 }}
          src={zifoLogoImage}
        />
        <Typography
          variant="h6"
          noWrap
          component="a"
          href="/"
          sx={{
            mr: 2,
            display: { xs: "none", md: "flex" },
            fontWeight: 700,
            fontFamily: "monospace",
            color: "inherit",
            textDecoration: "none",
          }}
        >
          Skills tracker
        </Typography>

        <Stack spacing={2} direction="row" sx={{ flexGrow: 1, ml: 1 }}>
          {pages.map((page) => (
            <Button
              sx={{ my: 2, mx: 0.5, color: "#2b2b2b" }}
              onClick={() => page.onClick()}
            >
              {page.name}
            </Button>
          ))}
        </Stack>

        <Box sx={{ flexGrow: 0 }}>
          <Tooltip title="Open settings">
            <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
              <Avatar
                alt={user?.userName.toUpperCase()}
                src="/static/images/avatar/2.jpg"
                sx={{ bgcolor: "#141a54" }}
              />
            </IconButton>
          </Tooltip>
          <Menu
            sx={{ mt: "45px" }}
            id="menu-appbar"
            anchorEl={anchorElUser}
            anchorOrigin={{
              vertical: "top",
              horizontal: "right",
            }}
            keepMounted
            transformOrigin={{
              vertical: "top",
              horizontal: "right",
            }}
            open={Boolean(anchorElUser)}
            onClose={handleCloseUserMenu}
          >
            {settings.map((setting) => (
              <MenuItem key={setting.name} onClick={() => setting.onClick()}>
                <Typography textAlign="center">{setting.name}</Typography>
              </MenuItem>
            ))}
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
}
export default ResponsiveAppBar;
