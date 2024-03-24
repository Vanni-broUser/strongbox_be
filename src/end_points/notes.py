from datetime import datetime
from sqlalchemy import func, and_

from ..database import Session
from ..database.schema import Note

from .decorators import error_catching_decorator


def notes_query(args) -> list[Note]:
  with Session() as session:
    query = session.query(Note).filter(
      Note.completed == ('completed' in args and args['completed'])
    )
    if 'main' in args:
      query = query.filter(
        Note.main == args['main']
      )
    if 'date' in args:
      date = datetime.strptime(args['date'], '%Y-%m-%d')
      query = query.filter(
        func.date(Note.datetime) == date.date()
      )
    elif 'start' in args and 'end' in args:
      start = datetime.strptime(args['start'], '%Y-%m-%d')
      end = datetime.strptime(args['end'], '%Y-%m-%d')
      query = query.filter(
        and_(
          func.date(Note.datetime) > start.date(),
          func.date(Note.datetime) < end.date(),
        )
      )
    return query.all()


# Da testare
@error_catching_decorator
def get_notes_(args):
  return [note.to_dict() for note in notes_query(args)], 200
