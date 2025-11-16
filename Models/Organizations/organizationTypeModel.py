from sqlalchemy import Column, Integer, String, Date, ForeignKey
from Config.database import Base
from sqlalchemy.orm import relationship

class OrganizationTypes(Base):
    __tablenmame__ = "organizationtype"

    ORTP_PK = Column(Integer, primary_key=True, index=True)

    ORTP_name = Column(String(100), index=True, nullable=False)
    ORTP_description = Column(String(100), index=True, nullable=False)
    ORTP_date_create = Column(Date)

    organizations = relationship('Organizations', back_populates="type")
