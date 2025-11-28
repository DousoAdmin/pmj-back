from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from Config.database import Base


class UsersRolesOrganizations(Base):
    __tablename__ = "usersrolesorganizations"

    USRL_PK = Column(Integer, primary_key=True, autoincrement=True, index=True)
    USRL_date_create = Column(Date)
    USRL_date_update = Column(Date)
    USRL_user_create = Column(Integer, index=True)
    USRL_user_update = Column(Integer, index=True)
    USRL_state = Column(Integer, index=True)

    #ForeingKey
    USRL_FK_rol = Column(Integer, ForeignKey("roles.ROLE_PK"))
    USRL_FK_organization = Column(Integer, ForeignKey("organizations.ORGZ_PK"))
    USRL_FK_user = Column(Integer, ForeignKey("users.USER_PK"))

    #Relaciones
    user = relationship("User", back_populates="usersrolesorgani")
    organizations = relationship("Organizations", back_populates="usersrolesorganizations")
    roles = relationship("Roles", back_populates="usersrolesorgani")
