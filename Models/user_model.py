# models/user.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from Config.database import Base

class User(Base):
    __tablename__ = "users"

    USER_PK             = Column(Integer, primary_key=True, index=True, autoincrement=True)
    USER_FK_user_create = Column(Integer, nullable=True, index=True)
    USER_FK_user_update = Column(Integer, nullable=True, index=True )
    USER_username       = Column(String(255), unique=True, nullable=False)
    USER_password       = Column(String(255), nullable=False)

    USER_date_create    = Column(Date, nullable=True)
    USER_date_update    = Column(Date, nullable=True)
    

    USER_FK_state_user  = Column(Integer, nullable=True, index=True)
    USER_reset_password = Column(Integer, nullable=True)      # ej. flag/contador/código
    USER_address_ip     = Column(String(100), nullable=True)  # ajusta longitud si tu DDL usa otra
