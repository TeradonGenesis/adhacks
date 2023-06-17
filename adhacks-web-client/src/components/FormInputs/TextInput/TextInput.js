import { styled, TextField } from "@mui/material";
import React from "react";

const StyledTextField = styled(TextField)(({ theme }) => ({
  "& .MuiInputBase-root": {
    padding: theme.spacing(1),
    display: "flex",
    alignItems: "center",
  },

  "& .MuiOutlinedInput-root": {
    "& fieldset": {
      border: `1px solid ${theme.palette.border.main} !important`,
    },
  },

  "& .MuiInputBase-input": {
    margin: 0,
    padding: `0px ${theme.spacing(1)}`,
  },
}));

const TextInput = ({ TextFieldProps = {} }) => {
  return <StyledTextField {...TextFieldProps} />;
};

export default TextInput;
