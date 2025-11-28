from sqlalchemy import Column, Integer, String, Date, ForeignKey
from Config.database import Base
from sqlalchemy.orm import relationship

class Organizations(Base):
    __tablename__ = "organizations"

    ORGZ_PK = Column(Integer, primary_key=True, index=True)

    ORGZ_name = Column(String(100), index=True, nullable=False)
    ORGZ_descriptions = Column(String(100), index=True, nullable=False)
    ORGZ_nit = Column(String(100), index=True)
    ORGZ_creation_date = Column(String(100), index=True)

    ORGZ_FK_statu = Column(Integer, ForeignKey('organizationstatuses.ORST_PK'))
    ORGZ_FK_type = Column(Integer, ForeignKey('organizationtype.ORTP_PK'))

    status = relationship('OrganizationStatuses', back_populates="organizations")
    type =  relationship('OrganizationsTypes', back_populates="organizations")
    usersrolesorganizations = relationship('UserRolesOrganiciones', back_populates="organizations")
    organizationapproaches = relationship('OrganizationsApproaches', back_populates="organizations")
    organizationdocumentS = relationship('OrganizationDocument', back_populates="organizations")