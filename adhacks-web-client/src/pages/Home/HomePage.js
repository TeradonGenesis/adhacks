import { Box, styled } from "@mui/material";
import React from "react";

import ActionButton from "@/components/Buttons/ActionButton";
import TextInput from "@/components/FormInputs/TextInput";

const HomePageContainer = styled(Box)(({ theme }) => ({
  padding: `${theme.spacing(5)}`,
}));

const ToolbarContainer = styled(Box)(({ theme }) => ({
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
}));

const HomePage = () => {
  return (
    <HomePageContainer>
      <ToolbarContainer>
        <TextInput TextFieldProps={{ placeholder: "Search something" }} />

        <ActionButton label="Add company" variant="outlined" />
      </ToolbarContainer>

      <Box>table</Box>
    </HomePageContainer>
  );
};

export default HomePage;
