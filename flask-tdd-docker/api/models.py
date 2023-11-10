from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import Integer, String, ForeignKey, BIGINT

Base = declarative_base()

class users(Base):
    __tablename__ = 'users'
    
    user_id: Mapped[int] = mapped_column('user_id',Integer, primary_key=True)
    contact_name: Mapped[str] = mapped_column('contact_name',String(255))

    def __repr__(self) -> str:
        return f"<User(user_id={self.user_id!r}, name={self.contact_name!r})>"

class pictures(Base):
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

    image_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    picture_filename: Mapped[str] = mapped_column(String(255))
    timestamp: Mapped[int] = mapped_column(BIGINT)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))

    def __repr__(self) -> str:
        return f"<Picture(image_id={self.image_id!r}, picture_filename={self.picture_filename!r}, timestamp={self.timestamp!r}, user_id={self.user_id!r})>"


class status(Base):
    __tablename__ = 'status'

    status_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(String(255))
    timestamp: Mapped[int] = mapped_column(BIGINT)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'))

    def __repr__(self) -> str:
        return f"<Status(status_id={self.status_id!r}, status={self.status!r}, timestamp={self.timestamp!r}, user_id={self.user_id!r})>"