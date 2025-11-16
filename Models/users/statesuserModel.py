from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from Config.database import Base


class StatesUser(Base):
    __tablename__ = "stateuser"

    STTS_PK = Column(Integer, primary_key=True, index=True, autoincrement=True)
    STTS_name = Column(String(45), nullable=False, index=True)
    STTS_description = Column (String(45), index=True)
    STTS_date_create = Column (Date)

    #Relaciones
    user = relationship("User", back_populates="state_user")