from sqlalchemy import Column, Integer, String, ForeignKey, Date
from app.base import Base

class Company(Base):
    __tablename__ = 'company'
    
    CO_ID = Column(Integer,primary_key=True)
    CO_NAME = Column(String(4000),nullable=False)
    CO_DESCRIPTION = Column(String,nullable=False)
    CO_INDUSTRY_TYPE = Column(String,nullable=False)
    CO_SELLING_POINTS = Column(String,nullable=True)
    CO_BEST_STRATEGIES = Column(String,nullable=True)
    CO_COMPETITOR_SELLING_POINTS = Column(String,nullable=True)
    CO_COMPETITOR_BEST_STRATEGIES = Column(String,nullable=True)

    def __repr__(self):
        return f"<Company(name='{self.CO_NAME}', summary='{self.CO_DESCRIPTION}')>"


class Campaign(Base):
    __tablename__ = 'campaign'
    
    CA_ID = Column(Integer,primary_key=True)
    CA_CO_ID = Column(Integer,nullable=False,ForeignKey("Company.CO_ID"))
    CA_START_DATE = Column(Date,nullable=False)
    CA_END_DATE = Column(Date,nullable=False)
    CA_COMPANY_CAMPAIGN_INFO = Column(String,nullable=True)
    CA_COMPANY_COPY = Column(String(100),nullable=True)
    CA_URL = Column(String(255),nullable=False)
    CA_TARGET_MARKET = Column(String,nullable=False)
    CA_SOCIAL_MEDIA = Column(String,nullable=False)
    CA_TONE = Column(String,nullable=False)
    CA_PURPOSE = Column(String,nullable=False)
    
    def __repr__(self):
        return f"<Campaign(CA_ID='{self.CA_ID}')>"
    

class Advert(Base):
    __tablename__ = 'advert'
    
    AD_ID = Column(Integer,primary_key=True)
    AD_TYPE = Column(String,nullable=False)
    AD_DAY = Column(Integer,nullable=False)
    AD_TIME = Column(Integer,nullable=False)
    AD_COPY = Column(Integer,nullable=False)
    AD_HASHTAGS = Column(String,nullable=False)
    AD_LEAD_LINK = Column(Integer,nullable=False)
    AD_CA_ID = Column(Integer,nullable=False,ForeignKey("Campaign.CA_ID"))
    
    def __repr__(self):
        return f"<Advert(AD_ID='{self.AD_ID}')>"