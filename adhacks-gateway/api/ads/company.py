from sqlalchemy import Column, Integer, String
from app.base import Base

class Company(Base):
    __tablename__ = 'company'
    
    CO_ID = Column(Integer,primary_key=True)
    CO_NAME = Column(String(4000),nullable=False)
    CO_DESCRIPTION = Column(String,nullable=False)
    CO_WEB_INFO = Column(String,nullable=False)
    CO_URL = Column(String(255),nullable=False)
    CO_INDUSTRY_TYPE = Column(String,nullable=False)
    CO_SELLING_POINTS = Column(String,nullable=False)
    CO_BEST_STRATEGIES = Column(String,nullable=False)
    CO_COMPETITOR_SELLING_POINTS = Column(String,nullable=False)
    CO_COMPETITOR_BEST_STRATEGIES = Column(String,nullable=False)

    
    def __repr__(self):
        return f"<Company(name='{self.CO_NAME}', summary='{self.CO_DESCRIPTION}')>"