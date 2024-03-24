from ...database import Session
from ...database.schema import User


def get_user_by_mail(mail: str) -> User:
  with Session() as session:
    return session.query(User).filter(
      User.mail == mail
    ).first()


def get_user_by_pass_token(pass_token: str) -> User:
  with Session() as session:
    return session.query(User).filter(
      User.pass_token == pass_token
    ).first()
