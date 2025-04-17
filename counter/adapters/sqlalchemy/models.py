from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ObjectCount(Base):
    __tablename__ = 'object_counts'

    id = Column(Integer, primary_key=True)
    object_type = Column(String(255))
    count = Column(Integer)
    timestamp = Column(TIMESTAMP)

    def __repr__(self):
        return f"<ObjectCount(id={self.id}, object_type={self.object_type}, count={self.count}, timestamp={self.timestamp})>"
