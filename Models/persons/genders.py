from sqlalchemy import Column, String, Integer, Date, BINARY, ForeignKey
from Config.database import Base
from sqlalchemy.orm import relationship

class Genders(Base):
    __tablename__ = "genders"

    GNDR_PK = Column(Integer, primary_key=True, unique=True)
    GNDR_name = Column(String(45), index=True, nullable=False)
    GNDR_description = Column(String(155), index=True)
    GNDR_state = Column(Integer)

    #Relaciones
    person = relationship("Persons", back_populates="gender")