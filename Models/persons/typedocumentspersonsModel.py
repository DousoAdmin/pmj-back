from sqlalchemy import Column, Integer, String, Date
from Config.database import Base
from sqlalchemy.orm import relationship


class TypeDocumentsPersons(Base):
    __tablename__ = "typedocumentspersons"

    TPDU_PK = Column(Integer, primary_key=True, autoincrement=True)
    TPDU_name = Column(String(50), nullable=False)
    TPDU_code = Column(String(10), nullable=False)
    TPDU_description = Column(String(255))
    TPDU_date_create = Column(Date)
    TPDU_user_create = Column(Integer)

    persons = relationship("Persons", back_populates="typedocument")
