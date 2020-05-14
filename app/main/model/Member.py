from dataclasses import dataclass
from sqlalchemy.orm import relationship
from .. import db


class Member(db.Model):
    __tablename__ = "member"

    member_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nric = db.Column(db.CHAR(9), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.SmallInteger, nullable=False, default=1, server_default="0")
    dob = db.Column(db.Date, nullable=False)
    annual_income = db.Column(db.Float, unique=False, nullable=False, default=0, server_default="0")
    occupation_type = db.Column(db.SmallInteger, nullable=False, default=0, server_default="0")
    marital_status = db.Column(db.SmallInteger, nullable=False, default=1, server_default="0")
    spouse_nric = db.Column(db.CHAR(9), nullable=True)
    households = relationship("HouseholdMember", back_populates="member")

    def __repr__(self):
        return "<Member '{}'>".format(self.member_id)
