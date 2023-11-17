from flask import jsonify
from app.api import bp
from app.models import users, status
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

@bp.route('/users/<int:user_id>', methods=['GET'])
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

# get all status of a user
@bp.route('/users/<int:user_id>/status', methods=['GET'])
def get_user_status(user_id):
    status_list = db.session.query(status).filter(status.user_id==user_id).all()
    data = [status.to_dict() for status in status_list]
    if not status_list:
        return jsonify({
            'status': 'fail',
            'message': 'User does not exist'
        })
    else:
        return jsonify({
            'status': 'success',
            'data': {
                'user_id': user_id,
                'contact_name': status_list[0].user.contact_name,   
                'status': data
            }
        })

# get all status
@bp.route('/status', methods=['GET'])
def get_all_status():
    status_list = db.session.query(status).all()
    data = [status.to_dict() for status in status_list]
    if not status_list:
        return jsonify({
            'status': 'fail',
            'message': 'No status in database'
        })
    else:
        return jsonify({
            'status': 'success',
            'data': {
                'status': data
            }
        })
