from sqlalchemy import Column, Integer, String, Date, ForeignKey
from Config.database import Base
from sqlalchemy.orm import relationship

class OrganizationStatuses(Base):
    __tablename__ = "organizationstatuses"

    ORST_PK = Column(Integer, primary_key=True, index=True)
    ORST_name = Column(String(100), index=True, nullable=False)
    ORST_description = Column(String(100), index=True, nullable=False)
    ORST_date_create = Column(Date)

    organizations = relationship('Organizations', back_populates="status")