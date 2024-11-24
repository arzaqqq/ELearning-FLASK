# models/student.py
from models import db
from flask_login import UserMixin
import hashlib

class StudentModel(db.Model, UserMixin):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=True)  # Tambahkan kolom nomor HP

    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password == StudentModel.hash_password(password)

    def get_id(self):
        return str(self.id)
