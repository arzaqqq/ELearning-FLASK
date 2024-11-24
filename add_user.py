from models import db
from models.user import UserModel, hash_password
from app import app  # Pastikan app diimport

with app.app_context():
    # Tambah pengguna baru
    username = "Miftahul Arzaq"
    password = hash_password("mirza12345")
    role = "admin"  # atau "user"

    new_user = UserModel(username=username, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()

    print(f"Pengguna {username} berhasil ditambahkan!")
