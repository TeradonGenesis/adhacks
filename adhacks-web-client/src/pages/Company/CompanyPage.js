import { Box, styled, useTheme } from "@mui/material";
import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { json, useNavigate, useParams } from "react-router-dom";

import ActionButton from "@/components/Buttons/ActionButton";
import SelectInput from "@/components/FormInputs/SelectInput";
import TextInput from "@/components/FormInputs/TextInput";
import Section from "@/components/Section";
import { industryOptions } from "@/utils/companyPageUtils";
import GenerateCampaignForm from "./GenerateCampaignForm";

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
  const { id } = useParams();
  const [isGenerateFormShown, setIsGenerateFormShown] = useState(false);

  const { control, handleSubmit } = useForm({
    defaultValues: {
      name: "",
      website: "",
      industryType: null,
      description: "",
    },
  });

  const onSubmit = ({ name, website, industryType, description }) => {
    fetch("http://127.0.0.1:5000/public/api/v1/ads/companies/create", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        co_name: name,
        co_url: website,
        co_description: industryType.value,
        industry_type: description,
      }),
    })
      .then((res) => {
        console.log(res);
      })
      .catch((error) => console.log({ error }));
  };

  if (isGenerateFormShown) {
    return (
      <GenerateCampaignForm onCancel={() => setIsGenerateFormShown(false)} />
    );
  }

  return (
    <CompanyPageContainer>
      <Box sx={{ width: "100%", maxWidth: "800px" }}>
        {id && (
          <Box
            sx={{
              display: "flex",
              justifyContent: "flex-end",
              marginBottom: theme.spacing(4),
            }}
          >
            <ActionButton
              label="Generate new campaign"
              variant="outlined"
              color={theme.palette.secondary.main}
              onClick={() => setIsGenerateFormShown(true)}
            />
          </Box>
        )}

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
              <TextInput
                control={control}
                controlName="name"
                TextFieldProps={{ placeholder: "Company name" }}
              />
            </Section>

            <Section
              required
              label="Website"
              SectionContainerProps={{ sx: { flex: 1 } }}
            >
              <TextInput
                control={control}
                controlName="website"
                TextFieldProps={{ placeholder: "Company website" }}
              />
            </Section>
          </DualColumn>

          <Section required label="Industry type">
            <SelectInput SelectProps={{ options: industryOptions }} />
          </Section>

          <Section
            required
            label="Description"
            description="Describe the company and what it does"
          >
            <TextInput
              control={control}
              controlName="description"
              TextFieldProps={{
                multiline: true,
                minRows: 4,
                placeholder: "Describe the company and what it does ...",
              }}
            />
          </Section>

          <ButtonContainer>
            <ActionButton
              label="Reset"
              color={theme.palette.grey[500]}
              ButtonProps={{ sx: { width: "150px" } }}
            />
            <ActionButton
              label="Submit"
              ButtonProps={{ sx: { width: "150px" } }}
              onClick={handleSubmit(onSubmit)}
            />
          </ButtonContainer>
        </Section>
      </Box>
    </CompanyPageContainer>
  );
};

export default CompanyPage;
