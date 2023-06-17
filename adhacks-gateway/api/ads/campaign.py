from sqlalchemy import Column, Integer, String, ForeignKey
from app.base import Base

class Campaign(Base):
    __tablename__ = 'campaign'
    
    CA_ID = Column(Integer,primary_key=True)
    CA_CO_ID = Column(Integer,primary_key=True,ForeignKey("Company.CO_ID"))
    CA_COMPANY_CAMPAIGN_INFO = Column(String,nullable=True)
    CA_COMPANY_COPY = Column(String(100),nullable=False)
    CA_TARGET_MARKET = Column(String,nullable=False)
    CA_TONE = Column(String,nullable=False)
    
    def __repr__(self):
        return f"<Campaign(CA_ID='{self.CA_ID}')>"