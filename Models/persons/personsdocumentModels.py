from sqlalchemy import Column, String, Integer, Date, BINARY, ForeignKey
from Config.database import Base
from sqlalchemy.orm import relationship


class PersonsDocument(Base):
    __tablename__ = "personsdocuments"

    PRDC_PK = Column(Integer, primary_key=True, unique=True)
    PRDC_name = Column(String(155), index=True, nullable=False)
    PRDC_location = Column(String(255), index=True, nullable=False)

    # Conexion
    PRDC_FK_state = Column(Integer, ForeignKey("statepersondoc.STPD_PK"))
    PRDC_FK_person = Column(Integer, ForeignKey("persons.PRSN_PK"))
    PRDC_FK_document = Column(Integer, ForeignKey("documents.DCMT_PK"))

    #Relaciones de ForeingKey
    state = relationship("StatePersonDoc", back_populates="persondocument")
    person = relationship("Persons", back_populates="persondocument")
    document = relationship("Documents", back_populates="persondocument")

    