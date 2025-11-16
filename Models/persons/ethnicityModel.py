from sqlalchemy import Column, String, Integer, Date, BINARY, ForeignKey
from Config.database import Base
from sqlalchemy.orm import relationship


class Ethnicity(Base):
    __tablename__ = "ethnicity"

    ETNC_PK = Column(Integer, primary_key=True, unique=True)
    ETNC_name = Column(String(45), index=True, nullable=False)
    ETNC_description = Column(String(155), index=True)
    ETNC_state = Column(BINARY)

    #Relaciones
    person = relationship("Persons", back_populates="ethnicity")