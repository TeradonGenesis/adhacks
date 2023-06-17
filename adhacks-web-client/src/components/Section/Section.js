import { Box, Typography, styled } from "@mui/material";
import React from "react";

const Label = styled(Typography)(({ theme }) => ({
  fontWeight: "bold",
  fontSize: "1.2rem",
}));

const Description = styled(Typography)(({ theme }) => ({
  fontWeight: "bold",
  fontSize: "0.9rem",
  color: theme.palette.grey[600],
}));

const Error = styled(Typography)(({ theme }) => ({
  color: theme.palette.alert.main,
}));

const Section = ({
  children,
  label,
  required,
  description,
  error,
  SectionContainerProps = {},
  ChildrenContainerProps = {},
}) => {
  return (
    <Box {...SectionContainerProps}>
      <Label>
        {label} {required && "*"}
      </Label>

      {description && <Description>{description}</Description>}

      <Box {...ChildrenContainerProps}>{children}</Box>

      {error && <Error>error</Error>}
    </Box>
  );
};

export default Section;
