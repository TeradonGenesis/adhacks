from langchain import OpenAI, PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader
import openai
from typing import List

from .models import Company, Campaign, Advert
from .repositories import CompanyRepository, CampaignRepository, AdvertRepository

class CompanyService:
    def __init__(self, company_repository: CompanyRepository, api_key: str):
        self.company_repository = company_repository
        self.llm = OpenAI(temperature=0, openai_api_key=api_key)
        self.text_splitter = CharacterTextSplitter()
        openai.api_key = api_key
    
    def create_company(self, name: str, description: str, website: str, industry_type: str) -> Company:
        company = Company(CO_NAME=name, CO_DESCRIPTION=description, CO_WEBSITE=website, CO_INDUSTRY_TYPE=industry_type)
        self.company_repository.add(company)
        return company
    
    def get_company_by_id(self, id: str) -> Company:
        return self.company_repository.get_by_id(id)
    
    def get_all_companies(self) -> List[Company]:
        return self.company_repository.get_all()
    
    def update_company(self, company: Company, company: str) -> str:
        return self.company_repository.update_company(company, company)


class CampaignService:
    def __init__(self, campaign_repository: CampaignRepository, api_key: str):
        self.campaign_repository = campaign_repository
        self.llm = OpenAI(temperature=0, openai_api_key=api_key)
        self.text_splitter = CharacterTextSplitter()
        openai.api_key = api_key
    
    def create_campaign(self, comp_id: str, start_date: str, end_date: str, comp_camp_info: str, comp_copy: str, link: str, target_market: str, social_media: str, tone: str, purpose: str, city: str) -> Campaign:
        campaign = Campaign(CA_CO_ID=comp_id, CA_START_DATE=start_date, CA_END_DATE=end_date, CA_COMPANY_CAMPAIGN_INFO=comp_camp_info, CA_COMPANY_COPY=comp_copy, CA_URL=link, CA_TARGET_MARKET=target_market, CA_SOCIAL_MEDIA=social_media, CA_TONE=tone, CA_PURPOSE=purpose, CA_CITY=city)
        self.campaign_repository.add(campaign)
        return campaign
    
    def get_campaign_by_co_id(self, co_id: str) -> Campaign:
        return self.campaign_repository.get_by_id(co_id)
    
    def get_all_companies(self) -> List[Campaign]:
        return self.campaign_repository.get_all()


class AdvertService:
    def __init__(self, advert_repository: AdvertRepository, api_key: str):
        self.advert_repository = advert_repository
        self.llm = OpenAI(temperature=0, openai_api_key=api_key)
        self.text_splitter = CharacterTextSplitter()
        openai.api_key = api_key
    
    def create_advert(self, CO_NAME: str, CO_DESCRIPTION: str, CO_WEBSITE: str, CO_INDUSTRY_TYPE: str) -> Advert:
        advert = Advert(CO_NAME=CO_NAME, CO_DESCRIPTION=CO_DESCRIPTION, CO_WEBSITE=CO_WEBSITE, CO_INDUSTRY_TYPE=CO_INDUSTRY_TYPE)
        self.advert_repository.add(advert)
        return advert
    
    def get_advert_by_id(self, id: str) -> Advert:
        return self.advert_repository.get_by_id(id)
    
    def get_all_adverts(self) -> List[Advert]:
        return self.advert_repository.get_all()
    
    def update_summary(self, advert: Advert, summary: str) -> str:
        return self.advert_repository.update_summary(advert, summary)