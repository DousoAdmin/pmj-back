from sqlalchemy import Column, String, Integer, Date, BINARY, ForeignKey
from Config.database import Base
from sqlalchemy.orm import relationship


class Documents(Base):
    __tablename__ = "documents"

    DCMT_PK = Column(Integer, primary_key=True, unique=True)
    DCMT_name = Column(String(45), index=True, nullable=False)
    DCMT_description = Column(String(255), index=True)

    # ForeingKey
    DCMT_FK_state = Column(Integer, ForeignKey("ducumentstate.DCST_PK"))

    # Relaciones
    persondocument = relationship("PersonsDocument", back_populates="document")
    documentstate = relationship("DocumentStates", back_populates="document")