from models import db
from flask_login import UserMixin
import hashlib

# Fungsi untuk hashing password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    username = db.Column(db.String(80), unique=True, nullable=False)  # Unique Username
    password = db.Column(db.String(120), nullable=False)  # Hashed Password
    role = db.Column(db.String(20), nullable=False, default='user')  # User Role (default: 'user')

    # Method untuk memeriksa password
    def check_password(self, password):
        return self.password == hash_password(password)

    # Flask-Login memerlukan get_id untuk mengidentifikasi user
    def get_id(self):
        return str(self.id)  # Pastikan mengembalikan id sebagai string

    # Representasi string untuk debugging
    def __repr__(self):
        return f"<User {self.username}, Role: {self.role}>"
