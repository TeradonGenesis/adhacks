import { Box, styled } from "@mui/material";
import React from "react";
import { useNavigate } from "react-router-dom";

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
  const navigate = useNavigate();

  const handleAddCompany = () => {
    navigate("/company/new");
  };

  const handleViewCompany = () => {
    navigate("/company/dedwed");
  };

  return (
    <Box>
      <ToolbarContainer>
        <TextInput
          TextFieldProps={{
            placeholder: "Search something",
            sx: { width: "300px" },
          }}
        />

        <ActionButton
          label="Add company"
          variant="outlined"
          onClick={handleAddCompany}
        />
      </ToolbarContainer>

      <Table onRowClick={handleViewCompany} />
    </Box>
  );
};

export default HomePage;
