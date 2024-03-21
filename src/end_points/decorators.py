import traceback


def error_catching_decorator(func):

  def wrapper(*args):
    try:
      return func(*args)
    except Exception:
      traceback.print_exc()
      return {'error': 'Qualcosa è andato storto'}, 500

  # Serve davvero?
  wrapper.__name__ = func.__name__
  return wrapper
