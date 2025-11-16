from sqlalchemy import Column, String, Integer, Date, BINARY, ForeignKey
from Config.database import Base
from sqlalchemy.orm import relationship

class StatePersonDoc(Base):
    __tablename__ = "statepersondoc"

    STPD_PK = Column(Integer, primary_key=True, unique=True)
    STPD_name = Column(String(45), index=True, nullable=True)
    STPD_description = Column(String(100), index=True)
    STPD_date_create = Column (Date)

    #RELACIONES
    persondocument = relationship("PersonsDocument", back_populates="state")