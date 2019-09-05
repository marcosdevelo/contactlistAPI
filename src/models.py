from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(120), unique=True, nullable=False)


    def __repr__(self):
        return '<Person %r>' % self.email

    def serialize(self):
        return {
            "id":self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            }