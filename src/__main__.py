from flask import Flask, request, jsonify

from .costants import DATABASE_URL
from .database import set_database

from .end_points.crud import (
  create_instance_,
  update_instance_,
  delete_instance_,
  get_instance_by_id_
)


app = Flask(__name__)


# CRUD

@app.route('/instances/<string:class_name>', methods=['POST'])
def create_instance(class_name):
  instance, error, status_code = create_instance_(class_name, request.json)
  if error:
    return jsonify(error), status_code
  return jsonify(instance.serialize()), status_code


@app.route('/instances/<string:class_name>/<int:instance_id>', methods=['GET'])
def get_instance_by_id(class_name, instance_id):
  instance, error, status_code = get_instance_by_id_(class_name, instance_id)
  if error:
    return jsonify(error), status_code
  return jsonify(instance.serialize()), status_code


@app.route('/instances/<string:class_name>/<int:instance_id>', methods=['PATCH'])
def update_instance(class_name, instance_id):
  instance, error, status_code = update_instance_(class_name, instance_id, request.json)
  if error:
    return jsonify(error), status_code
  return jsonify(instance.serialize()), status_code


@app.route('/instances/<string:class_name>/<int:instance_id>', methods=['DELETE'])
def delete_instance(class_name, instance_id):
  response, error, status_code = delete_instance_(class_name, instance_id)
  if error:
    return jsonify(error), status_code
  return jsonify(response), status_code


if __name__ == '__main__':
  set_database(DATABASE_URL)
  app.run(host='0.0.0.0', port=8080)
