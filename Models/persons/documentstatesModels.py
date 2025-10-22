from sqlalchemy import Column, String, Integer, Date, BINARY, ForeignKey
from Config.database import Base
from sqlalchemy.orm import relationship


class DocumentStates(Base):
    __tablename__ = "documentstate"

    DCST_PK = Column(Integer, primary_key=True, unique=True)
    DCST_name = Column(String(45), index=True, nullable=False)
    DCST_description = Column(String(155), index=True)

    #Relaciones 
    document = relationship("Documents", back_populates="documentstate")