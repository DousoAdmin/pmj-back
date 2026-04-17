from sqlalchemy import Column, Integer, String, Date, ForeignKey
from Config.database import Base
from sqlalchemy.orm import relationship


class OrganizationDocumentType(Base):
    __tablename__ = "organizationdocumenttype"

    ODPT_PK = Column(Integer, primary_key=True, index=True)
    ODPT_name = Column(String(100), nullable=False) 
    ODPT_description = Column(String(100), nullable=False)
    ODPT_date_create = Column(Date)
    ODPT_user_create = Column(Date)
    ODPT_user_update = Column(Date)

    organizationdocumentS = relationship('OrganizationDocument', back_populates="organidocumenttype")
