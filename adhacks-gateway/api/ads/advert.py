from sqlalchemy import Column, Integer, String, ForeignKey
from app.base import Base

class Advert(Base):
    __tablename__ = 'advert'
    
    AD_ID = Column(Integer,primary_key=True)
    AD_COPY = Column(Integer,primary_key=False)
    AD_TYPE = Column(String,nullable=False)
    AD_CA_ID = Column(String,nullable=False)
    
    def __repr__(self):
        return f"<Advert(AD_ID='{self.AD_ID}')>"