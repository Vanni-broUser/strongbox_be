import requests

from .costants import GENERIC_HOSTNAME


def send_mail(mail, body, subject):
  response = requests.post(f'{GENERIC_HOSTNAME}send-mail', json={
    'body': body,
    'email': mail,
    'subject': subject
  })
  if response.json()['status'] != 'ok':
    raise ValueError(f'Mail error to {mail}')
