import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from flask_login import UserMixin

class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    email = sa.Column(sa.String, nullable=True)
    token = sa.Column(sa.String, nullable=True)
    hash_password = sa.Column(sa.String, nullable=True)
    score = sa.Column(sa.String, nullable=True)
