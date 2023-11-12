from flask import jsonify
from app.api import bp
from app.models import users
from app import db
from sqlalchemy import select

@bp.route('/users', methods=['GET'])
def get_users():
    users_list = db.session.query(users).all()
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

@bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
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