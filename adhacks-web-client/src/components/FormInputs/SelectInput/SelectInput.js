import { useTheme } from "@mui/material";

import React, { useMemo } from "react";
import Select from "react-select";

const SelectInput = ({ SelectProps = {} }) => {
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

  return <Select styles={styles} {...SelectProps} />;
};

export default SelectInput;
