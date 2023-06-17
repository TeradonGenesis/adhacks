import DoneIcon from "@mui/icons-material/Done";
import EditIcon from "@mui/icons-material/Edit";
import EngineeringIcon from "@mui/icons-material/Engineering";
import { Box, styled, useTheme } from "@mui/material";
import React from "react";

const GenerationStepsContainer = styled(Box)(({ theme }) => ({
  display: "flex",
  gap: "30px",
  alignItems: "center",
}));

const IconContainer = styled(Box)(({ theme }) => ({
  width: "80px",
  height: "80px",
  border: `4px solid ${theme.palette.grey[400]}`,
  borderRadius: "50%",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
}));

const stepArray = [
  { stepNumber: 1, Icon: EditIcon },
  { stepNumber: 2, Icon: EngineeringIcon },
  { stepNumber: 3, Icon: DoneIcon },
];

const GenerationSteps = ({ currentStepNumber = 1 }) => {
  const theme = useTheme();

  return (
    <GenerationStepsContainer>
      {stepArray.map((step, index) => {
        const { stepNumber, Icon } = step;
        const shouldHighlightStep = currentStepNumber >= stepNumber;

        return (
          <React.Fragment key={stepNumber}>
            {index !== 0 && (
              <Box
                sx={{
                  width: "200px",
                  border: `1px solid ${theme.palette.grey[400]}`,
                  ...(shouldHighlightStep && {
                    borderColor: theme.palette.process.main,
                  }),
                }}
              />
            )}

            <IconContainer
              sx={{
                ...(shouldHighlightStep && {
                  borderColor: theme.palette.process.main,
                }),
              }}
            >
              <Icon
                sx={{
                  fontSize: "50px",
                  color: shouldHighlightStep
                    ? theme.palette.process.main
                    : theme.palette.grey[400],
                }}
              />
            </IconContainer>
          </React.Fragment>
        );
      })}
    </GenerationStepsContainer>
  );
};

export default GenerationSteps;
