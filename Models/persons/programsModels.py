from sqlalchemy import Column, String, Integer, Date, BINARY, ForeignKey
from Config.database import Base
from sqlalchemy.orm import relationship

class Program(Base):
    __tablename__ = "programs"

    PRGM_PK = Column(Integer, primary_key=True, unique=True)
    PRGM_name = Column(String(45), index=True, nullable=False)
    PRGM_description = Column(String(255), index=True)
    PRGM_state = Column(Integer)

    #Relaciones
    beneficiarys = relationship("Beneficiary", back_populates="program")