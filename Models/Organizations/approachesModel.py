from sqlalchemy import Column, Integer, String, Date, ForeignKey
from Config.database import Base
from sqlalchemy.orm import relationship

class Approaches(Base):
    __tablename__ = "approaches"

    APCH_PK = Column(Integer, primary_key=True, index=True)
    APCH_name = Column(String(100), index=True, nullable=False)
    APCH_description = Column(String(100), index=True, nullable=False)
    APCH_date_create = Column(Date)

    organizationappreaches = relationship('OrganizationsApproaches', back_populates="approaches")