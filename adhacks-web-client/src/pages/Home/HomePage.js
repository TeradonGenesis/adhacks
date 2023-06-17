import { Box, styled } from "@mui/material";
import React from "react";

import ActionButton from "@/components/Buttons/ActionButton";

const HomePageContainer = styled(Box)(({ theme }) => ({
  padding: `${theme.spacing(5)}`,
}));

const ToolbarContainer = styled(Box)(({ theme }) => ({
  display: "flex",
  justifyContent: "space-between",
}));

const HomePage = () => {
  return (
    <HomePageContainer>
      <ToolbarContainer>
        <Box>Search</Box>
        <Box>
          <ActionButton label="Add company" variant="outlined" />
        </Box>
      </ToolbarContainer>

      <Box>table</Box>
    </HomePageContainer>
  );
};

export default HomePage;
