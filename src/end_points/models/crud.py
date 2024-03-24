from ...database.schema import *
from ...database.operations import create, get_by_id, update, delete

from ..decorators import error_catching_decorator


ALLOWED_CLASSES = ['Note', 'Tag']


def allowed_classes_control(func):

  def wrapper(class_name, *args):
    if class_name in ALLOWED_CLASSES:
      return func(globals().get(class_name), *args)
    else:
      return {'error': f'Class {class_name} not allowed'}, 400

  return wrapper


@error_catching_decorator
@allowed_classes_control
def create_instance_(class_type, data):
  return create(class_type, data['params']).to_dict(), 201


@error_catching_decorator
@allowed_classes_control
def update_instance_(class_type, instance_id, data):
  instance = get_by_id(class_type, instance_id)
  if instance is None:
    return {'error': f'{class_type.__name__} with id {instance_id} not found'}, 404

  return update(instance, data['params']).to_dict(), 200


@error_catching_decorator
@allowed_classes_control
def delete_instance_(class_type, instance_id):
  instance = get_by_id(class_type, instance_id)
  if instance is None:
    return {'error': f'{class_type.__name__} with id {instance_id} not found'}, 404

  delete(instance)
  return {'message': f'{class_type.__name__} with id {instance_id} deleted successfully'}, 200


@error_catching_decorator
@allowed_classes_control
def get_instance_by_id_(class_type, instance_id):
  instance = get_by_id(class_type, instance_id)
  if instance is None:
    return {'error': f'{class_type.__name__} with id {instance_id} not found'}, 404

  return instance.to_dict(), 200
