from flask import jsonify
from app.main import bp
from app.models import users
from app import db
from sqlalchemy import select

@bp.route('/')
@bp.route('/index')
def index():
    return "Hello, Worddldd!"