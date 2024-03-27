from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Text, Integer, String, DateTime, Boolean, ForeignKey, func


Base = declarative_base()


class BaseEntity(Base):
  __abstract__ = True

  id = Column(Integer, primary_key=True, autoincrement=True)
  created_at = Column(DateTime(timezone=True), default=func.now())
  updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

  def to_dict(self):
    dict_obj = {}
    for attribute in self.__dict__:
      if getattr(self, attribute) is not None and attribute != '_sa_instance_state':
        dict_obj[attribute] = getattr(self, attribute)
    return dict_obj

  def __repr__(self):
    attributes = [f'{attr}: {getattr(self, attr)}' for attr in self.to_dict()]
    return f'{self.__class__.__name__} {{{", ".join(attributes)}}}'


class Note(BaseEntity):
  __tablename__ = 'note'

  content = Column(Text)
  title = Column(String, nullable=False)
  datetime = Column(DateTime(timezone=True))
  main = Column(Boolean, nullable=False, default=False)
  daily = Column(Boolean, nullable=False, default=False)
  completed = Column(Boolean, nullable=False, default=False)
  user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

  user = relationship('User', back_populates='note')
  note_tag = relationship('NoteTag', back_populates='note')
  note_document = relationship('NoteDocument', back_populates='note')


class User(BaseEntity):
  __tablename__ = 'user'

  password = Column(String)
  pass_token = Column(String)
  mail = Column(String, nullable=False)
  name = Column(String, nullable=False)

  tag = relationship('Tag', back_populates='user')
  note = relationship('Note', back_populates='user')
  document = relationship('Document', back_populates='user')


class Tag(BaseEntity):
  __tablename__ = 'tag'

  name = Column(String, nullable=False)
  user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

  user = relationship('User', back_populates='tag')
  note_tag = relationship('NoteTag', back_populates='tag')


class NoteTag(BaseEntity):
  __tablename__ = 'note_tag'

  tag_id = Column(Integer, ForeignKey('tag.id'), nullable=False)
  note_id = Column(Integer, ForeignKey('note.id'), nullable=False)

  tag = relationship('Tag', back_populates='note_tag')
  note = relationship('Note', back_populates='note_tag')


class Document(BaseEntity):
  __tablename__ = 'document'

  title = Column(String, nullable=False)
  description = Column(Text)
  user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

  user = relationship('User', back_populates='document')
  note_document = relationship('NoteDocument', back_populates='document')


class NoteDocument(BaseEntity):
  __tablename__ = 'note_document'

  note_id = Column(Integer, ForeignKey('note.id'), nullable=False)
  document_id = Column(Integer, ForeignKey('document.id'), nullable=False)

  note = relationship('Note', back_populates='note_document')
  document = relationship('Document', back_populates='note_document')
