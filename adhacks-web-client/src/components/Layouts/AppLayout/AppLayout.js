import { Box, Typography, styled } from "@mui/material";
import React from "react";
import { Outlet } from "react-router-dom";

const HeaderContainer = styled(Box)(({ theme }) => ({
  backgroundColor: theme.palette.primary.main,
  height: "80px",
  display: "flex",
  alignItems: "center",
  padding: `0px ${theme.spacing(3)}`,
}));

const HeaderText = styled(Typography)(({ theme }) => ({
  color: theme.palette.common.white,
  fontWeight: "bold",
  fontSize: "2rem",
}));

const OutletContainer = styled(Box)(({ theme }) => ({
  padding: `${theme.spacing(5)}`,
}));

const AppLayout = () => {
  return (
    <Box>
      <HeaderContainer>
        <HeaderText>Holy Pandas</HeaderText>
      </HeaderContainer>

      <OutletContainer>
        <Outlet />
      </OutletContainer>
    </Box>
  );
};

export default AppLayout;
