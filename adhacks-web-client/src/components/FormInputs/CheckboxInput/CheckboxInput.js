import { Box, Checkbox, Typography } from "@mui/material";
import React from "react";

const CheckboxInput = ({ label }) => {
  return (
    <Box sx={{ display: "flex", alignItems: "center", gap: "5px" }}>
      <Checkbox />
      <Typography>{label}</Typography>
    </Box>
  );
};

export default CheckboxInput;
