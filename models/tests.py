import sqlalchemy as sa
from .db_session import SqlAlchemyBase

class Test(SqlAlchemyBase):
    __tablename__ = 'tests'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    text = sa.Column(sa.String, nullable=True)
    startcode = sa.Column(sa.String, nullable=True)
    input = sa.Column(sa.String, nullable=True)
    output = sa.Column(sa.String, nullable=True)
    use = sa.Column(sa.String, nullable=True)
    complete = sa.Column(sa.String, nullable=True)
    say = sa.Column(sa.String, nullable=True)
