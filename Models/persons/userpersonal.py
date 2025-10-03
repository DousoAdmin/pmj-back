# models/user.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from Config.database import Base

class UserPersonas(Base):
    __tablename__ = "userspersonas"

    USPS_PK = Column(Integer, primary_key=True, index=True, autoincrement=True)
    USPS_state = Column(Integer, nullable=True, index=True)
    USPS_date_create = Column(Date, nullable=True)
    USPS_date_update = Column(Date, nullable=True)

    # Llave
    USPS_FK_create = Column(Integer,nullable=True )
    USPS_FK_update = Column(Integer,nullable=True )
    USPS_FK_user = Column(Integer)
    USPS_FK_person = Column(Integer, ForeignKey("persons.PRSN_PK"))

    # Relaciones
    person = relationship("Person", back_populates="userspersons")