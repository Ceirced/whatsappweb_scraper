from flask import Flask, jsonify
from .models import users, pictures, status
from flask_restx import Resource
from . import db
       
# get user by id

class get_user(Resource):   
    def get(self, user_id):
        user = db.session.query(users).filter_by(user_id=user_id).first()
        if not user:
            return jsonify({
                'status': 'fail',
                'message': 'User does not exist'
            })
        else:
            return jsonify({
                'status': 'success',
                'data': {
                    'user_id': user.user_id,
                    'contact_name': user.contact_name
                }
            })   