from ...database import Session
from ...database.schema import Tag

from ..decorators import error_catching_decorator


def tags_query(args) -> list[Tag]:
  with Session() as session:
    query = session.query(Tag)
    return query.all()


@error_catching_decorator
def get_tags_(args):
  return [tag.to_dict() for tag in tags_query(args)], 200
