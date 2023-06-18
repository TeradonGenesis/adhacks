import { styled, TextField } from "@mui/material";
import React from "react";
import { Controller } from "react-hook-form";

const StyledTextField = styled(TextField)(({ theme }) => ({
  "& .MuiInputBase-root": {
    padding: theme.spacing(1),
    display: "flex",
    alignItems: "center",
  },

  "& .MuiOutlinedInput-root": {
    "& fieldset": {
      border: `1px solid ${theme.palette.border.main} !important`,
      borderRadius: "5px",
    },
  },

  "& .MuiInputBase-input": {
    margin: 0,
    padding: `0px ${theme.spacing(1)}`,
  },
}));

const TextInput = ({ control, controlName, TextFieldProps = {} }) => {
  if (!control) {
    return <StyledTextField fullWidth {...TextFieldProps} />;
  }

  return (
    <Controller
      control={control}
      name={controlName}
      render={({ field }) => {
        const { value, onChange } = field;

        return (
          <StyledTextField
            fullWidth
            value={value}
            onChange={(event) => onChange(event.target.value)}
            {...TextFieldProps}
          />
        );
      }}
    />
  );
};

export default TextInput;
