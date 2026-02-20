from sqlalchemy import Column, Integer, String, Date, ForeignKey
from Config.database import Base
from sqlalchemy.orm import relationship


class OrganizationObservations(Base):
    __tablename__ = "organizationobservation"

    OROB_PK = Column(Integer, primary_key=True, index=True)

    OROB_FK_document = Column(Integer, ForeignKey('organizationdocument.ORDC_PK'))

    OROB_comment = Column(String(100), index=True)
    OROB_status = Column(String(100), index=True)
    OROB_date_create = Column(Date)
    OROB_user_create = Column(Date) 

    organizationdocumentS = relationship('OrganizationDocument', back_populates="organiobsevation")