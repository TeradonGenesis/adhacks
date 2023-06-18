import { Box, styled, useTheme } from "@mui/material";
import React from "react";
import { useForm } from "react-hook-form";

import ActionButton from "@/components/Buttons/ActionButton";
import CheckboxInput from "@/components/FormInputs/CheckboxInput";
import DateInput from "@/components/FormInputs/DateInput";
import SelectInput from "@/components/FormInputs/SelectInput";
import TextInput from "@/components/FormInputs/TextInput";
import Section from "@/components/Section";
import { cityOptions, toneOptions } from "@/utils/companyPageUtils";
import GenerationSteps from "./GenerationSteps";

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

  const { control, handleSubmit } = useForm({
    defaultValues: {
      tone: "",
      city: null,
      duration: { from: null, to: null },
      targetAudience: "",
      objectives: "",
    },
  });

  const onSubmit = ({ tone, city, duration, targetAudience, objectives }) => {
    fetch(
      "http://127.0.0.1:5000/public/api/v1/ads/companies/1001/campaigns/generate",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tone,
          city,
          start_date: "",
          end_date: "",
          target_market: targetAudience,
          campaign_purpose: objectives,
          link: "",
          social_media: "instagram",
          lead_conv_enabled: false,
        }),
      }
    )
      .then((res) => {
        console.log(res);
      })
      .catch((error) => console.log({ error }));
  };

  return (
    <GenerateCampaignFormContainer>
      <GenerationSteps />

      <Box sx={{ width: "100%", maxWidth: "800px", marginTop: "40px" }}>
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
              <SelectInput
                control={control}
                controlName="tone"
                SelectProps={{ options: toneOptions }}
              />
            </Section>

            <Section
              required
              label="City"
              SectionContainerProps={{ sx: { flex: 1 } }}
            >
              <SelectInput
                control={control}
                controlName="city"
                SelectProps={{ options: cityOptions }}
              />
            </Section>
          </DualColumn>

          <Section label="Campaign duration" required>
            <DualColumn>
              <Section
                required
                label="From"
                SectionContainerProps={{ sx: { flex: 1 } }}
              >
                <DateInput control={control} controlName="duration.from" />
              </Section>

              <Section
                required
                label="To"
                SectionContainerProps={{ sx: { flex: 1 } }}
              >
                <DateInput control={control} controlName="duration.to" />
              </Section>
            </DualColumn>
          </Section>

          <Section
            label="Target audience"
            required
            description="Describe the target audience for this campaign"
          >
            <TextInput
              control={control}
              controlName="targetAudience"
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
              control={control}
              controlName="objectives"
              TextFieldProps={{
                multiline: true,
                minRows: 4,
                placeholder: "My objective is to ....",
              }}
            />
          </Section>

          {/* <Section
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
          </Section> */}

          {/* <Section
            label="Enable link conversion bot"
            ChildrenContainerProps={{ sx: { width: "200px" } }}
          >
            <SelectInput />
          </Section> */}

          <ButtonContainer>
            <ActionButton
              label="Cancel"
              color={theme.palette.grey[500]}
              ButtonProps={{ sx: { width: "150px" } }}
              onClick={onCancel}
            />
            <ActionButton
              label="Submit"
              ButtonProps={{ sx: { width: "150px" } }}
              onClick={handleSubmit(onSubmit)}
            />
          </ButtonContainer>
        </Section>
      </Box>
    </GenerateCampaignFormContainer>
  );
};

export default GenerateCampaignForm;
