from flask import jsonify, render_template, request, url_for, redirect, flash
from app.main import bp
from app.models import users, status
from app import db
from sqlalchemy import select
from datetime import datetime


@bp.route('/')
@bp.route('/index')
def index():
    return "Feed"

@bp.route('/profile/<string:username>')
def profile(username):
    user = users.query.filter_by(contact_name=username).first_or_404()
    pictures = user.pictures
    status = user.status

    return render_template('profile.html', 
                           user=user, pictures=pictures, 
                           status=status)