from .database import db


class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(), nullable = False, unique = True)
    password = db.Column(db.String(), nullable = False)
    type = db.Column(db.String(), default = "general")
    trans = db.relationship("Transaction", backref = "creator")

class Transaction(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    t_name = db.Column(db.String(), nullable = False)
    t_search_name = db.Column(db.String(), nullable = False)
    t_type = db.Column(db.String(), nullable = False)
    t_date = db.Column(db.String(), nullable = False)
    delivery_date = db.Column(db.String(), default = "To be updated")
    s_city = db.Column(db.String(), nullable = False)
    d_city = db.Column(db.String(), nullable = False)
    internal_status = db.Column(db.String(), default = "requested")
    delivery_status = db.Column(db.String(), default = "in-process")
    decription = db.Column(db.String())
    amount = db.Column(db.Integer(), default = 1000)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))


# user_1.trans

# trans_1.creator => <user_1>