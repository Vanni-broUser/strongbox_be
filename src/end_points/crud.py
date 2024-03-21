from ..database.schema import *
from ..database.operations import create, get_by_id, update, delete

from .decorators import error_catching_decorator


ALLOWED_CLASSES = ['Note']


def allowed_classes_control(func):

  def wrapper(class_name, *args):
    if class_name in ALLOWED_CLASSES:
      return func(globals().get(class_name), *args)
    else:
      return None, {'error': f'Class {class_name} not allowed'}, 400

  return wrapper


@error_catching_decorator
@allowed_classes_control
def create_instance_(class_type, data):
  return create(class_type, data['params']), None, 201


@error_catching_decorator
@allowed_classes_control
def update_instance_(class_type, instance_id, update_params):
  instance = get_by_id(class_type, instance_id)
  if instance is None:
    return None, {'error': f'{class_type.__name__} with id {instance_id} not found'}, 404

  return update(instance, update_params), None, 200


@error_catching_decorator
@allowed_classes_control
def delete_instance_(class_type, instance_id):
  instance = get_by_id(class_type, instance_id)
  if instance is None:
    return None, {'error': f'{class_type.__name__} with id {instance_id} not found'}, 404

  delete(instance)
  return {'message': f'{class_type.__name__} with id {instance_id} deleted successfully'}, None, 200


@error_catching_decorator
@allowed_classes_control
def get_instance_by_id_(class_type, instance_id):
  instance = get_by_id(class_type, instance_id)
  if instance is None:
    return None, {'error': f'{class_type.__name__} with id {instance_id} not found'}, 404

  return instance, None, 200
