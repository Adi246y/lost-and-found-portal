from models.database import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    status = db.Column(db.String(10))  # lost / found
    location = db.Column(db.String(100))
    date = db.Column(db.String(50))
    image = db.Column(db.String(200))
    user_id = db.Column(db.Integer)