from models import db

class UiuxModel(db.Model):  # Pastikan ini sesuai
    __tablename__ = 'uiux_designer'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(50), nullable=False)

    def __init__(self, title, image, duration, price):
        self.title = title
        self.image = image
        self.duration = duration
        self.price = price

    def __repr__(self):
        return f"<UiuxModel {self.title}>"
