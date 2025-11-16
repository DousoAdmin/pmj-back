from sqlalchemy import Column, Integer, String, Date, ForeignKey
from Config.database import Base
from sqlalchemy.orm import relationship


class OrganizationDocument(Base):
    __tablename__ = "organizationdocument"

    ORDC_PK = Column(Integer, primary_key=True, index=True)

    ORDC_FK_organization = Column(Integer, ForeignKey('organizations.ORGZ_PK'))
    ORDC_FK_document_type = Column(Integer, ForeignKey('organizationdocumenttype.ODTP_PK'))

    ORDC_file_path = Column(String(100), index=True)
    ORDC_original_name = Column(String(100), index=True)
    ORDC_upload_date = Column(Date)
    ORDC_state = Column(String(100), index=True)
    ORDC_observation = Column(String(100), index=True)
    ORDC_user_create = Column(String(100), index=True) 

    organizations = relationship('Organizations', back_populates="organizationdocumentS")
    organidocumenttype = relationship('OrganizationDocumentType', back_populates="organizationdocumentS")
    organiobsevation = relationship('OrganizationObservations', back_populates="organizationdocumentS")