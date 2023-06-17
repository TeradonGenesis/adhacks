import { styled, Typography, useTheme } from "@mui/material";
import React, { useMemo } from "react";

const ActionButton = ({
  label,
  variant = "filled",
  color,
  ButtonProps = {},
  LabelProps = {},
  onClick,
}) => {
  const theme = useTheme();
  const { ActionButtonContainer, Label } = useMemo(() => {
    const isFilled = variant === "filled";
    const selectedColor = color || theme.palette.secondary.main;

    const ActionButtonContainer = styled("button")(({ theme }) => ({
      backgroundColor: isFilled ? selectedColor : theme.palette.common.white,

      padding: `${theme.spacing(1)} ${theme.spacing(2)}`,
      borderRadius: "30px",
      border: isFilled ? "unset" : `2px solid ${selectedColor}`,
    }));

    const Label = styled(Typography)(({ theme }) => ({
      fontWeight: "bold",
      fontSize: "1.2rem",
      color: isFilled ? theme.palette.common.white : selectedColor,
    }));

    return { ActionButtonContainer, Label };
  }, [variant, color, theme]);

  return (
    <ActionButtonContainer onClick={onClick} {...ButtonProps}>
      <Label {...LabelProps}>{label}</Label>
    </ActionButtonContainer>
  );
};

export default ActionButton;
