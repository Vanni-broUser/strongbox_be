from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Text, Integer, String, DateTime, func


Base = declarative_base()


class BaseEntity(Base):
  __abstract__ = True

  id = Column(Integer, primary_key=True, autoincrement=True)
  created_at = Column(DateTime(timezone=True), default=func.now())
  updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

  def serialize(self):
    dict_obj = {}
    for attribute in self.__dict__:
      if getattr(self, attribute) is not None and attribute != '_sa_instance_state':
        dict_obj[attribute] = getattr(self, attribute)
    return dict_obj

  def __repr__(self):
    attributes = [f'{attr}: {getattr(self, attr)}' for attr in self.serialize()]
    return f"{self.__class__.__name__} {{{', '.join(attributes)}}}"


class Note(BaseEntity):
  __tablename__ = 'note'

  content = Column(Text)
  title = Column(String, nullable=False)
