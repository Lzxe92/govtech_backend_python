from .. import db


class HouseholdMember(db.Model):
    __tablename__ = "household_member"

    household_id = db.Column('household_id', db.Integer, db.ForeignKey('household.household_id'), primary_key=True)
    member_id = db.Column('member_id', db.Integer, db.ForeignKey('member.member_id'), primary_key=True)
    # household = db.relationship("Household", back_populates="member")
    # member = db.relationship("Member", back_populates="household")

    household = db.relationship("Household",
                            backref=db.backref("household_member",
                                            cascade="all, delete-orphan")
                            )
    member = db.relationship("Member")

    # Accepts as positional arguments as well
    def __init__(self, member=None, household=None):
        self.member = member
        self.household = household
