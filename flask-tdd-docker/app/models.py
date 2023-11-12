from sqlalchemy.orm import Mapped, mapped_column, declarative_base, column_property
from sqlalchemy import Integer, String, ForeignKey, BIGINT
from app import db
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property


Base = declarative_base()


def format_timestamp(timestamp) -> str:
    return datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y %H:%M:%S')

class users(db.Model):
    __tablename__ = 'users'
    user_id= db.Column(db.Integer, primary_key=True)
    contact_name = db.Column(db.String(255), nullable=False, unique=True)
    pictures = db.relationship('pictures', backref='user', lazy='dynamic')
    status = db.relationship('status', backref='user', lazy='dynamic')

    

    def __repr__(self) -> str:
        return f"<User(user_id={self.user_id!r}, contact_name={self.contact_name!r})>"

class pictures(db.Model):
    """Class used to represent a the pictures table in the database
    
    Attributes:
    ------------
    image_id: Mapped[int]
        The id of the picture

    picture_filename: Mapped[str]
        The filename of the picture

    timestamp: Mapped[int]
        unix timestamp of when the picture was saved

    user_id: Mapped[int]
        The id of the user the picture belongs to
    
    """
    __tablename__ = 'pictures'

    image_id = db.Column(db.Integer, primary_key=True)
    picture_filename: Mapped[str] = mapped_column(String(255))
    timestamp = db.Column(db.Integer)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))
    formatted_timestamp = column_property(format_timestamp)
    
    @hybrid_property
    def formatted_timestamp(self) -> str:
        return format_timestamp(self.timestamp)

    def __repr__(self) -> str:
        return f"<Picture(image_id={self.image_id!r}, picture_filename={self.picture_filename!r}, timestamp={self.timestamp!r}, user_id={self.user_id!r})>"


class status(db.Model):
    __tablename__ = 'status'

    status_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column('status',String(255))
    timestamp: Mapped[int] = mapped_column(BIGINT)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))

    @hybrid_property
    def formatted_timestamp(self) -> str:
        return format_timestamp(self.timestamp)

    def __repr__(self) -> str:
        return f"<Status(status_id={self.status_id!r}, status={self.status!r}, timestamp={self.timestamp!r}, user_id={self.user_id!r})>"

users_contact_name_index = db.Index('contact_name', users.contact_name, unique=True)
status_status_index = db.Index('status',status.status, status.timestamp, status.user_id, unique=True)
pictures_picture_filename_index = db.Index('picture_filename', pictures.picture_filename, pictures.timestamp, pictures.user_id, unique=True)


if __name__ =="__main__":
    users_contact_name_index.create(db.engine)
    status_status_index.create(db.engine)
    pictures_picture_filename_index.create(db.engine)