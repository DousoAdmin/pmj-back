from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from Config.database import Base


class Permissions(Base):
    __tablename__ = "permissions"

    PRMS_PK = Column(Integer, primary_key=True, autoincrement=True, index=True)
    PRMS_name = Column(String(45), index=True, nullable=False)
    PRMS_description = Column(String(100), index=True, nullable=False)
    PRMS_system_name = Column(String(45), index=True, nullable=False)
    PRMS_date_create = Column(Date, index=True)
    PRMS_date_update = Column(Date, index=True)
    PRMS_user_create = Column(Integer, index=True)
    PRMS_user_update = Column(Integer, index=True)

    #Relaciones
    rolespermission = relationship("RolesPermissions", back_populates="permission")