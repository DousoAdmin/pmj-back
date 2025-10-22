from sqlalchemy import Column, Integer, String, BINARY
from Config.database import Base
from sqlalchemy.orm import relationship


class Disabilitys(Base):
    __tablename__ = "disabilitys"

    DSBT_PY = Column(Integer, primary_key=True, unique=True)
    DSBT_name = Column(String(45), index=True)
    DSBT_description = Column(String(150), index=True)
    DSBT_state = Column(BINARY)

    person = relationship("Persons", back_populates="disability")
