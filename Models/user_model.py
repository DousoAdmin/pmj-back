from sqlalchemy import Column, Integer, String
from Config.database import Base

class User(Base):
    __tablename__ = "users"  # Debe coincidir con tu tabla

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)