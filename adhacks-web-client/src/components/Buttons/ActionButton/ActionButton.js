import { styled, Typography } from "@mui/material";
import React, { useMemo } from "react";

const ActionButton = ({
  label,
  variant = "filled",
  ContainerProps = {},
  LabelProps = {},
}) => {
  const { ActionButtonContainer, Label } = useMemo(() => {
    const isFilled = variant === "filled";

    const ActionButtonContainer = styled("button")(({ theme }) => ({
      backgroundColor: isFilled
        ? theme.palette.primary.main
        : theme.palette.common.white,

      padding: `${theme.spacing(1)} ${theme.spacing(2)}`,
      borderRadius: "30px",
      border: isFilled ? "unset" : `2px solid ${theme.palette.primary.main}`,
    }));

    const Label = styled(Typography)(({ theme }) => ({
      fontWeight: "bold",
      fontSize: "1.2rem",
      color: isFilled ? theme.palette.common.white : theme.palette.primary.main,
    }));

    return { ActionButtonContainer, Label };
  }, [variant]);

  return (
    <ActionButtonContainer {...ContainerProps}>
      <Label {...LabelProps}>{label}</Label>
    </ActionButtonContainer>
  );
};

export default ActionButton;
