import uuid
from datetime import datetime

from ...database.schema import User
from ...database.operations import create, update

from ...utils import send_mail
from ..decorators import error_catching_decorator
from .queries import get_user_by_mail, get_user_by_pass_token


@error_catching_decorator
def register_user_(data):
  email = data['email']
  if get_user_by_mail(email):
    return {'status': 'ko', 'error': 'Email già in uso'}, 409

  user = create(
    User, {
      'email': email,
      'name': data['name'],
      'pass_token': str(uuid.uuid4())
    })

  send_mail(
    user.mail,
    f"""
      Ciao Bro!\n
      Per concludere la tua iscrizione crea una password con questo link:
      https://strongboxfe-hosting23232323.replit.app/#/password/{user.pass_token} 🚀\n\n
      Ci sentiamo presto,\n
      Vanni
    """,
    'Registrazione su Strongbox'
  )
  return {
    'status': 'ok',
    'message': 'Hai ricevuto una mail per verificare il tuo account e proseguire la registrazione'
  }, 200


@error_catching_decorator
def login_(data, session_data):
  email = data['email']
  user = get_user_by_mail(email)
  if not user:
    return {'status': 'ko', 'error': 'Utente non trovato'}, 404

  if user.mail != email or user.password != data['password']:
    return {'status': 'ko', 'error': 'Credenziali errate'}, 401

  session_id = str(uuid.uuid4())
  session_data[session_id] = {'timestamp': datetime.now(), 'bot_id': user.id}
  return {'status': 'ok', 'user_id': user.id, 'session_token': session_id}, 200


@error_catching_decorator
def ask_change_password_(data):
  user = get_user_by_mail(data['email'])
  if not user:
    return {'status': 'ko', 'error': 'Utente non trovato'}, 404

  user: User = update(user, {'pass_token': str(uuid.uuid4())})

  send_mail(
    user.mail,
    f"""
      Ciao Bro,\n
      Per procedere con il reset della password, clicca sul seguente link:
      https://strongboxfe-hosting23232323.replit.app/#/password/{user.pass_token}\n\n
      Ci sentiamo presto,\n
      Vanni
    """,
    'Richiesta di Reset Password per Strongbox'
  )
  return {'status': 'ok', 'message': 'Mail per cambio password inviata'}, 200


@error_catching_decorator
def change_password_(data):
    user = get_user_by_pass_token(data['pass_token'])
    if not user:
      return {'status': 'ko', 'error': 'Questa pagina è scaduta'}, 404

    update(user, {
      'password': data['new_password'],
      'pass_token': None
    })
    return {'status': 'ok', 'message': 'Password aggiornata con successo'}, 200
