from sqlalchemy.ext.associationproxy import association_proxy

from .. import db


class Household(db.Model):
    __tablename__ = "household"

    household_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.SmallInteger, unique=False, nullable=True, default=1, server_default="1")
    members = association_proxy('household_member', 'member')
