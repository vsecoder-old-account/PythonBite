import sqlalchemy as sa
from .db_session import SqlAlchemyBase

class Forum(SqlAlchemyBase):
    __tablename__ = 'forums'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    title = sa.Column(sa.String, nullable=True)
    lesson = sa.Column(sa.String, nullable=True)
    quest = sa.Column(sa.String, nullable=True)
    results = sa.Column(sa.String, nullable=True)
    user = sa.Column(sa.String, nullable=True)
