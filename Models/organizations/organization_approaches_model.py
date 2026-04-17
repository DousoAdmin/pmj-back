from sqlalchemy import Column, Integer, String, Date, ForeignKey
from Config.database import Base
from sqlalchemy.orm import relationship


class OrganizationsApproaches(Base):
    __tablename__ = "organizationapproaches"

    ORAP_PK = Column(Integer, primary_key=True, index=True)

    ORAP_FK_organization = Column(Integer, ForeignKey('organizations.ORGZ_PK'))
    ORAP_FK_approach = Column(Integer, ForeignKey('approaches.APCH_PK'))

    ORAP_date_create = Column(String(100), index=True)
    ORAP_user_create = Column(String(100), index=True)

    organizations = relationship('Organizations', back_populates="organizationapproaches")
    approaches = relationship('Approaches', back_populates="organizationappreaches")

