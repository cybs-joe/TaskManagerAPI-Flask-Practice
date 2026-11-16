from . import db

class Task(db.Model):
    id = db.Column(db.Integer ,  primary_key=True)
    title = db.Column(db.String , nullable=False)
    description = db.Column(db.String(100) , nullable=False)
    completed = db.Column(db.Boolean , nullable=False , default=False)
    priority = db.Column(db.String(100) , nullable=False , default="medium")
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer , primary_key= True)
    username = db.Column(db.String , nullable = False)
    email = db.Column(db.String , nullable=False , unique = True)
    tasks = db.relationship('Task' , backref='user',lazy=True)
