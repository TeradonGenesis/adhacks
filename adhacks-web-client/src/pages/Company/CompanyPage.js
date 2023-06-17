import { Box, styled, useTheme } from "@mui/material";
import React from "react";

import ActionButton from "@/components/Buttons/ActionButton";
import TextInput from "@/components/FormInputs/TextInput";
import Section from "@/components/Section";

const CompanyPageContainer = styled(Box)(({ theme }) => ({
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
}));

const DualColumn = styled(Box)(({ theme }) => ({
  display: "flex",
  gap: theme.spacing(2),
}));

const ButtonContainer = styled(Box)(({ theme }) => ({
  display: "flex",
  gap: theme.spacing(2),
  justifyContent: "space-between",
  marginTop: theme.spacing(5),
}));

const CompanyPage = () => {
  const theme = useTheme();

  return (
    <CompanyPageContainer>
      <Box sx={{ width: "100%", maxWidth: "800px" }}>
        <Section
          label="Company details"
          description="Information about the company"
          ChildrenContainerProps={{
            sx: {
              display: "flex",
              flexDirection: "column",
              gap: theme.spacing(2),
              marginTop: theme.spacing(3),
            },
          }}
        >
          <DualColumn>
            <Section
              required
              label="Name"
              SectionContainerProps={{ sx: { flex: 1 } }}
            >
              <TextInput TextFieldProps={{ placeholder: "Company name" }} />
            </Section>

            <Section
              required
              label="Website"
              SectionContainerProps={{ sx: { flex: 1 } }}
            >
              <TextInput TextFieldProps={{ placeholder: "Company website" }} />
            </Section>
          </DualColumn>

          <Section required label="Industry type">
            <TextInput />
          </Section>

          <Section
            required
            label="Description"
            description="Describe the company and what it does"
          >
            <TextInput
              TextFieldProps={{
                multiline: true,
                minRows: 4,
                placeholder: "Describe the company and what it does ...",
              }}
            />
          </Section>

          <ButtonContainer>
            <ActionButton
              label="Cancel"
              ContainerProps={{
                sx: {
                  backgroundColor: theme.palette.grey[500],
                  width: "150px",
                },
              }}
            />
            <ActionButton
              label="Submit"
              ContainerProps={{ sx: { width: "150px" } }}
            />
          </ButtonContainer>
        </Section>
      </Box>
    </CompanyPageContainer>
  );
};

export default CompanyPage;
