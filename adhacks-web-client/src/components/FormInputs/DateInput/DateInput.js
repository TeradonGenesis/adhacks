import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import React from "react";
import { Controller } from "react-hook-form";

const DateInput = ({ control, controlName }) => {
  if (!control) {
    return (
      <LocalizationProvider dateAdapter={AdapterDayjs}>
        <DatePicker />
      </LocalizationProvider>
    );
  }

  return (
    <Controller
      control={control}
      name={controlName}
      render={({ field }) => {
        const { value, onChange } = field;

        return (
          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DatePicker value={value} onChange={(newVal) => onChange(newVal)} />
          </LocalizationProvider>
        );
      }}
    />
  );
};

export default DateInput;
