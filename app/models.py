from . import db

class Task(db.Model):
    id = db.Column(db.Integer ,  primary_key=True)
    title = db.Column(db.String , nullable=False)
    description = db.Column(db.String(100) , nullable=False)
    completed = db.Column(db.Boolean , nullable=False , default=False)
    priority = db.Column(db.String(100) , nullable=False , default="medium")

