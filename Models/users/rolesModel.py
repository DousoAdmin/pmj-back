from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from Config.database import Base

class Roles(Base):
    __tablename__ = "roles"

    ROLE_PK = Column(Integer, primary_key=True, autoincrement=True)
    ROLE_name = Column(String(45), nullable=False, index=True)
    ROLE_description = Column(String(255), nullable=False, index=True)
    ROLE_date_create = Column(Date, index=True)
    ROLE_date_update = Column(Date, index=True)
    ROLE_state = Column(Integer, index=True, nullable=False)

    #ForeingKey
    ROLE_FK_user_create = Column(Integer, ForeignKey(""))
    ROLE_FK_user_update = Column(Integer, ForeignKey(""))

    #Relaciones
    usersrolesorgani = relationship("UserRolesOrganiciones", back_populates="roles")
    rolespermission = relationship("RolesPermissions", back_populates="roles")
