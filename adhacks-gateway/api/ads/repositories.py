from typing import List
from sqlalchemy.orm import Session

from .models import Company
from .models import Campaign

class CompanyRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def add(self, company: Company) -> Company:
        self.session.add(company)
        self.session.commit()
        self.session.refresh(company)
        return company
    
    def get_by_id(self, co_id: str) -> Company:
        return self.session.query(Company).filter_by(co_id=co_id).first()
    
    def get_all(self) -> List[Company]:
        return self.session.query(Company).all()

    def update_company(self, company: Company, selling_points: str, best_strat: str, compet_sell_points: str, compet_best_strat: str) -> Company:
        company.CO_SELLING_POINTS = selling_points
        company.CO_BEST_STRATEGIES = best_strat
        company.CO_COMPETITOR_SELLING_POINTS = compet_sell_points
        company.CO_COMPETITOR_BEST_STRATEGIES = compet_best_strat
        self.session.commit()
        return company

class CampaignRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def add(self, campaign: Campaign) -> Campaign:
        self.session.add(campaign)
        self.session.commit()
        self.session.refresh(campaign)
        return campaign
    
    def get_by_co_id(self, co_id: str) -> Campaign:
        return self.session.query(Campaign).filter_by(ca_co_id=co_id).first()
    
    def get_all(self) -> List[Campaign]:
        return self.session.query(Campaign).all()

    def create_campaign(self, campaign: Campaign, comp_id: str, start_date: str, end_date: str, comp_camp_info: str, comp_copy: str, link: str, target_market: str, social_media: str, tone: str, purpose: str, city: str) -> str:
        campaign.CA_CO_ID = comp_id
        campaign.CA_START_DATE = start_date
        campaign.CA_END_DATE = end_date
        campaign.CA_COMPANY_CAMPAIGN_INFO = comp_camp_info
        campaign.CA_COMPANY_COPY = comp_copy
        campaign.CA_URL = link
        campaign.CA_TARGET_MARKET = target_market
        campaign.CA_SOCIAL_MEDIA = social_media
        campaign.CA_PURPOSE = purpose
        campaign.CA_TONE = tone
        campaign.CA_CITY = city
        self.session.commit()
        return campaign

class AdvertRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def add(self, advert: Advert) -> Advert:
        self.session.add(advert)
        self.session.commit()
        self.session.refresh(advert)
        return advert
    
    def get_by_id(self, ad_id: str) -> Advert:
        return self.session.query(Advert).filter_by(ad_id=ad_id).first()
    
    def get_all(self) -> List[Advert]:
        return self.session.query(Advert).all()
    
    def create_advert(self, advert: Advert, type: str, day: str, time: str, copy: str, hashtags: str, link: str, campaign_id: str) -> Advert
        advert.AD_TYPE = type
        advert.AD_DAY = day
        advert.AD_TIME = time
        advert.AD_COPY = copy
        advert.AD_HASHTAGS = hashtags
        advert.AD_LEAD_LINK = link
        advert.AD_CA_ID = campaign_id
        self.session.commit()
        return advert