from sqlalchemy import Column, Integer, String
from Config.database import Base
from sqlalchemy.orm import relationship


class Sexualidentitys(Base):
    __tablename__ = "sexulidentitys"

    SXID_PK = Column(Integer, primary_key=True, unique=True)
    SXID_name = Column(String(45), index=True, nullable=True)
    SXID_description = Column(String(250), index=True)

    #Relaciones
    person = relationship("Persons", back_populates="sexualidentity")