from sqlalchemy import Column, Integer, String, Date, ForeignKey
from Config.database import Base
from sqlalchemy.orm import relationship

class Persons(Base):
    __tablename__ = "persons"

    PRSN_PK = Column(Integer, primary_key=True, index=True)
    PRSN_name = Column(String(100), index=True, nullable=False )
    PRSN_lastname = Column(String(100), index=True, nullable=False)
    PRSN_phone = Column(String(45), index=True, unique=True, nullable=False)
    PRSN_email = Column(String(100), index=True, unique=True, nullable=False)
    PRSN_brithday = Column(Date, nullable=False)
    PRSN_identification = Column(String(45), index=True, unique=True, nullable=False)
    PRSN_location = Column(String(255), index=tuple, nullable=False)
    # PRSN_state se agregará cuando se cree la migración de base de datos
    # PRSN_state = Column(Integer, default=1, nullable=True, index=True)  # 1 = activo, 0 = inactivo

    # ForeingKey
    PRSN_FK_ethnicity = Column(Integer, ForeignKey("ethnicity.ETNC_PK"))
    PRSN_FK_disability = Column(Integer, ForeignKey("disabilitys.DSBT_PY"))
    PRSN_FK_gender = Column(Integer, ForeignKey("genders.GNDR_PK"))
    PRSN_FK_sexualidentity = Column(Integer, ForeignKey("sexulidentitys.SXID_PK"))   


    #Relaciones del ForeingKey
    ethnicity = relationship("Ethnicity", back_populates="person")
    disability = relationship("Disabilitys", back_populates="person")
    gender = relationship("Genders", back_populates="person")
    sexualidentity = relationship("Sexualidentitys", back_populates="person")


    #Relaciones de uno a muchos 
    userspersons = relationship("UserPersonas", back_populates="person")
    beneficiarys = relationship("Beneficiary", back_populates="person")
    persondocument = relationship("PersonsDocument", back_populates="person")

    
