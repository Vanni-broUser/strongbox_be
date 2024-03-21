from ..database import Session
from ..database.schema import Note

from .decorators import error_catching_decorator


def notes_query() -> list[Note]:
  with Session() as session:
    return session.query(Note).all()


# Da testare
@error_catching_decorator
def get_notes_():
  return [note.to_dict() for note in notes_query()], 200
