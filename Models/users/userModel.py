# models/user.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from Config.database import Base


class User(Base):
    __tablename__ = "users"

    USER_PK = Column(Integer, primary_key=True, index=True, autoincrement=True)
    USER_FK_user_create = Column(Integer, nullable=True, index=True)
    USER_FK_user_update = Column(Integer, nullable=True, index=True)
    USER_username = Column(String(255), unique=True, nullable=False, index=True)
    USER_password = Column(String(255), nullable=False)
    USER_date_create = Column(Date, nullable=True)
    USER_date_update = Column(Date, nullable=True)
    USER_reset_password = Column(Integer, nullable=True)
    USER_address_ip = Column(String(100), nullable=True)

    # ForeingKey
    USER_FK_state_user = Column(Integer,ForeignKey("stateuser.STTS_PK"))

    #Relaciones
    state_user = relationship("StatesUser", back_populates="user")
    userspersons = relationship("UserPersonas", back_populates="user")
    logs = relationship("Logs", back_populates="user")
    #usersrolesorgani = relationship("UserRolesOrganiciones", back_populates="user")
