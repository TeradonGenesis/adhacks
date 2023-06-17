import { Box, styled } from "@mui/material";
import React from "react";

import ActionButton from "@/components/Buttons/ActionButton";
import TextInput from "@/components/FormInputs/TextInput";
import Table from "@/components/Table";

const ToolbarContainer = styled(Box)(({ theme }) => ({
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  marginBottom: theme.spacing(5),
}));

const HomePage = () => {
  return (
    <Box>
      <ToolbarContainer>
        <TextInput TextFieldProps={{ placeholder: "Search something" }} />

        <ActionButton label="Add company" variant="outlined" />
      </ToolbarContainer>

      <Box>
        <Table />
      </Box>
    </Box>
  );
};

export default HomePage;
