from sqlalchemy import Column, Integer, Date, BINARY, ForeignKey
from Config.database import Base
from sqlalchemy.orm import relationship


class Beneficiary(Base):
    __tablename__ = "beneficiary"

    BNFC_PK = Column(Integer, primary_key=True, index=True)
    BNFC_state = Column(BINARY, index=True, nullable=False)
    BNFC_date_start = Column(Date)
    BNFC_date_finish = Column(Date)
    
    # Relaciones
    person_PRSN_PK = Column(Integer, ForeignKey("persons.PRSN_PK"))
    programs_PRGM_PK  = Column(Integer, ForeignKey("programs.PRGM_PK"))

    person = relationship("Persons", back_populates="beneficiarys")
    program = relationship("Program", back_populates="beneficiarys")
    
