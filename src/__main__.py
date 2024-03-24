from flask import Flask, request, jsonify
from flask_cors import CORS

from .costants import DATABASE_URL
from .database import set_database

from .end_points.models.crud import (create_instance_, update_instance_,
                              delete_instance_, get_instance_by_id_)
from .end_points.models.tags import get_tags_
from .end_points.models.notes import get_notes_
from .end_points.users import (register_user_, login_, ask_change_password_,
                               change_password_)

app = Flask(__name__)
CORS(app)
session_data = {}

# Generic CRUD


@app.route('/instances/<string:class_name>', methods=['POST'])
def create_instance(class_name):
  response, status_code = create_instance_(class_name, request.json)
  return jsonify(response), status_code


@app.route('/instances/<string:class_name>/<int:instance_id>', methods=['GET'])
def get_instance_by_id(class_name, instance_id):
  response, status_code = get_instance_by_id_(class_name, instance_id)
  return jsonify(response), status_code


@app.route('/instances/<string:class_name>/<int:instance_id>',
           methods=['PATCH'])
def update_instance(class_name, instance_id):
  response, status_code = update_instance_(class_name, instance_id,
                                           request.json)
  return jsonify(response), status_code


@app.route('/instances/<string:class_name>/<int:instance_id>',
           methods=['DELETE'])
def delete_instance(class_name, instance_id):
  response, status_code = delete_instance_(class_name, instance_id)
  return jsonify(response), status_code


# Notes


@app.route('/notes', methods=['GET'])
def get_notes():
  response, status_code = get_notes_(request.args)
  return jsonify(response), status_code


# Tag


@app.route('/tags', methods=['GET'])
def get_tags():
  response, status_code = get_tags_(request.args)
  return jsonify(response), status_code


# Users


@app.route('/register-user', methods=['POST'])
def register_user():
  response, status_code = register_user_(request.json)
  return jsonify(response), status_code


@app.route('/login', methods=['POST'])
def login():
  response, status_code = login_(request.json, session_data)
  return jsonify(response), status_code


@app.route('/ask-change-password', methods=['POST'])
def ask_change_password():
  response, status_code = ask_change_password_(request.json)
  return jsonify(response), status_code


@app.route('/change-password', methods=['POST'])
def change_password():
  response, status_code = change_password_(request.json)
  return jsonify(response), status_code


if __name__ == '__main__':
  set_database(DATABASE_URL)
  app.run(host='0.0.0.0', port=8080)
