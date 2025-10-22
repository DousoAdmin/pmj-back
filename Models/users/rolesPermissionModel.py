from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from Config.database import Base


class RolesPermissions(Base):
    __tablename__ = "rolespermission"

    RLPR_PK = Column(Integer, primary_key=True, autoincrement=True, index=True)
    RLPR_date_create = Column(Date, index=True)
    RLPR_date_update = Column(Date, index=True)
    RLPR_user_create = Column(Integer, index=True)
    RLPR_user_update = Column(Integer, index=True)
    RLPR_state = Column(Integer, index=True)

    #ForeingKey
    RLPR_FK_permission = Column(Integer, ForeignKey("permissions.PRMS_PK"))
    RLPR_FK_rol = Column(Integer, ForeignKey("roles.ROLE_PK"))

    #Relaciones
    permission = relationship("Permissions", back_populates="rolespermission")
    roles = relationship("Roles", back_populates="rolespermission")