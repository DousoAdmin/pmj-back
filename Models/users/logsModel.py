from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from Config.database import Base


class Logs(Base):
    __tablename__ = "logs"

    LOGS_PK = Column(Integer, primary_key=True, autoincrement=True, index=True)
    LOGS_action = Column(String(150), nullable=False, index=True)
    LOGS_description = Column(String(255), nullable=False, index=True)
    LOGS_timestamp = Column(DateTime(100), nullable=False, index=True)

    #ForeingKey
    LOGS_user_FK = Column(Integer, ForeignKey("users.USER_PK"))

    #Relacion
    user = relationship("User", back_populates="logs")
