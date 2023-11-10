from flask import Flask, jsonify
from .models import users, pictures, status
from flask_restx import Resource
from sqlalchemy import select
from . import db
       
# get user by id

class get_user(Resource):   
    def get(self, user_id):
        id, contact_name = db.session.execute(select(users.user_id,users.contact_name).where(users.user_id==user_id)).first()
        if not id and contact_name:
            return jsonify({
                'status': 'fail',
                'message': 'User does not exist'
            })
        else:
            return jsonify({
                'status': 'success',
                'data': {
                    'user_id': id,
                    'contact_name': contact_name
                }
            })   

# get all users
class get_all_users(Resource):
    def get(self):
        users_list = db.session.query(users).all()
        print({user.user_id:{'contact_name': user.contact_name} for user in users_list})
        if not users_list:
            return jsonify({
                'status': 'fail',
                'message': 'No users in database'
            })
        else:
            return jsonify({
                'status': 'success',
                'data': {
                    'users': {user.user_id:{'contact_name': user.contact_name} for user in users_list}
                }
            })