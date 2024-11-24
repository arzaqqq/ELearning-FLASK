from models import db

class TeacherModel(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    name = db.Column(db.String(100), nullable=False)  # Nama Guru
    expertise = db.Column(db.String(100), nullable=False)  # Keahlian
    image = db.Column(db.String(200), nullable=False)  # Nama file gambar
    linkedin = db.Column(db.String(200), nullable=True)  # URL LinkedIn
    facebook = db.Column(db.String(200), nullable=True)  # URL Facebook
    instagram = db.Column(db.String(200), nullable=True)  # URL Instagram

    # Representasi string untuk debugging
    def __repr__(self):
        return f"<Teacher {self.name}, Expertise: {self.expertise}>"
