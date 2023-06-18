import { useTheme } from "@mui/material";
import React, { useMemo } from "react";
import { Controller } from "react-hook-form";
import Select from "react-select";

const SelectInput = ({ control, controlName, SelectProps = {} }) => {
  const theme = useTheme();
  const styles = useMemo(() => {
    return {
      control: (provided, state) => {
        return {
          ...provided,
          border: `1px solid ${theme.palette.border.main} `,
          borderRadius: "5px",
          ":hover": { borderColor: theme.palette.border.main },
        };
      },
    };
  }, [theme]);

  if (!control) {
    return <Select styles={styles} {...SelectProps} />;
  }

  return (
    <Controller
      control={control}
      name={controlName}
      render={({ field }) => {
        const { value, onChange } = field;

        return (
          <Select
            styles={styles}
            value={value}
            onChange={(newVal) => onChange(newVal)}
            {...SelectProps}
          />
        );
      }}
    />
  );
};

export default SelectInput;
