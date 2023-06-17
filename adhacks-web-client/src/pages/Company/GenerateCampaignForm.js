import { Box, styled, useTheme } from "@mui/material";
import React from "react";

import ActionButton from "@/components/Buttons/ActionButton";
import CheckboxInput from "@/components/FormInputs/CheckboxInput";
import SelectInput from "@/components/FormInputs/SelectInput";
import TextInput from "@/components/FormInputs/TextInput";
import Section from "@/components/Section";

const GenerateCampaignFormContainer = styled(Box)(({ theme }) => ({
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

const GenerateCampaignForm = ({ onCancel }) => {
  const theme = useTheme();

  return (
    <GenerateCampaignFormContainer>
      <Box sx={{ width: "100%", maxWidth: "800px" }}>
        <Section
          label="Campaign information"
          description="Information that will help generate a campaign tailored for your business"
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
              label="Tone"
              SectionContainerProps={{ sx: { flex: 1 } }}
            >
              <SelectInput />
            </Section>

            <Section
              required
              label="City"
              SectionContainerProps={{ sx: { flex: 1 } }}
            >
              <SelectInput />
            </Section>
          </DualColumn>

          <Section label="Campaign duration" required>
            <DualColumn>
              <Section
                required
                label="From"
                SectionContainerProps={{ sx: { flex: 1 } }}
              >
                <TextInput />
              </Section>

              <Section
                required
                label="To"
                SectionContainerProps={{ sx: { flex: 1 } }}
              >
                <TextInput />
              </Section>
            </DualColumn>
          </Section>

          <Section
            label="Target audience"
            required
            description="Describe the target audience for this campaign"
          >
            <TextInput
              TextFieldProps={{
                multiline: true,
                minRows: 4,
                placeholder: "Describe the audience ...",
              }}
            />
          </Section>

          <Section
            label="Advertising objectives"
            required
            description="What are the objectives of this campaign?"
          >
            <TextInput
              TextFieldProps={{
                multiline: true,
                minRows: 4,
                placeholder: "My objective is to ....",
              }}
            />
          </Section>

          <Section
            label="Select your desired social channels"
            required
            description="Where would you like this campaign to run?"
            ChildrenContainerProps={{
              sx: { display: "flex", gap: "10px", marginTop: "10px" },
            }}
          >
            <CheckboxInput label="Instagram" />
            <CheckboxInput label="Twitter" />
            <CheckboxInput label="Facebook" />
          </Section>

          <Section
            label="Enable link conversion bot"
            ChildrenContainerProps={{ sx: { width: "200px" } }}
          >
            <SelectInput />
          </Section>

          <ButtonContainer>
            <ActionButton
              label="Cancel"
              ButtonProps={{
                sx: {
                  backgroundColor: theme.palette.grey[500],
                  width: "150px",
                },
              }}
              onClick={onCancel}
            />
            <ActionButton
              label="Submit"
              ButtonProps={{ sx: { width: "150px" } }}
            />
          </ButtonContainer>
        </Section>
      </Box>
    </GenerateCampaignFormContainer>
  );
};

export default GenerateCampaignForm;
