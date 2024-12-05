from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db
from models.user import UserModel
from models.teacher import TeacherModel
from models.course import CourseModel
from models.frontend import FrontendModel
from models.backend import BackendModel
from models.uiux import UiuxModel
from models.mobile import MobileModel
from models.student import StudentModel
from controllers.student_controller import student_register, student_login, student_logout
from controllers.teacher_controller import admin_teacher, edit_teacher, delete_teacher
from controllers.course_controller import admin_courses, edit_course, delete_course
from controllers.frontend_controller import admin_frontend, add_frontend, edit_frontend, delete_frontend
from controllers.backend_controller import admin_backend, add_backend, edit_backend, delete_backend
from controllers.uiux_controller import admin_uiux, add_uiux, edit_uiux, delete_uiux
from controllers.mobile_controller import admin_mobile, add_mobile, edit_mobile, delete_mobile
from controllers.message_controller import save_message
from flask_migrate import Migrate
from functools import wraps
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Konfigurasi Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/aezaqcourse'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inisialisasi
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

# Hashing password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Routes Front-end
@app.route('/')
def home():
    courses = CourseModel.query.all()
    teachers = TeacherModel.query.all()
    return render_template('index.html', courses=courses, teachers=teachers)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        return save_message()
    return render_template('contact.html')


@app.route('/admin/messages')
@login_required
def admin_messages():
    from models.message import MessageModel
    messages = MessageModel.query.all()  # Ambil semua pesan dari database
    return render_template('admin/messages.html', messages=messages)

@app.route('/admin/messages/delete/<int:id>', methods=['GET'])
@login_required
def delete_message(id):
    from models.message import MessageModel
    message = MessageModel.query.get_or_404(id)  # Cari pesan berdasarkan ID
    db.session.delete(message)  # Hapus pesan dari database
    db.session.commit()  # Simpan perubahan
    flash('Pesan berhasil dihapus!', 'success')  # Berikan feedback kepada user
    return redirect(url_for('admin_messages'))  # Kembali ke halaman daftar pesan



@app.route('/course')
def course():
    courses = CourseModel.query.all()  # Ambil semua kursus dari database
    return render_template('course.html', courses=courses)  # Kirim data kursus ke template

@app.route('/kursus-frontend')
def kursus_frontend():
    frontends = FrontendModel.query.all()
    return render_template('kursus_frontend.html', frontends=frontends)

@app.route('/kursus-backend')
def kursus_backend():
    backends = BackendModel.query.all()
    return render_template('kursus_backend.html', backends=backends)

@app.route('/kursus-uiux')
def kursus_uiux():
    uiuxs = UiuxModel.query.all()
    return render_template('kursus_uiux.html', uiuxs=uiuxs)

@app.route('/kursus-mobile')
def kursus_mobile():
    mobiles = MobileModel.query.all()
    return render_template('kursus_mobile.html', mobiles=mobiles)




@app.route('/teacher')
def teacher():
    teachers = TeacherModel.query.all()
    return render_template('teacher.html', teachers=teachers)



# Routes Admin Teacher (CRUD)
@app.route('/admin/teacher', methods=['GET', 'POST'])
def admin_teacher_route():
    return admin_teacher()

@app.route('/admin/teacher/edit/<int:id>', methods=['GET', 'POST'])
def edit_teacher_route(id):
    return edit_teacher(id)

@app.route('/admin/teacher/delete/<int:id>')
def delete_teacher_route(id):
    return delete_teacher(id)


#ROUTE FRONT-END
# Route untuk menampilkan semua data frontend developer
@app.route('/admin/frontend', methods=['GET', 'POST'])
@login_required
def admin_frontend_route():
    return admin_frontend()

# Route untuk menambahkan frontend developer baru
@app.route('/admin/frontend/add', methods=['GET', 'POST'])
@login_required
def add_frontend_route():
    return add_frontend()

# Route untuk mengedit frontend developer
@app.route('/admin/frontend/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_frontend_route(id):
    return edit_frontend(id)

# Route untuk menghapus frontend developer
@app.route('/admin/frontend/delete/<int:id>')
@login_required
def delete_frontend_route(id):
    return delete_frontend(id)


#ROUTE back-END
# Route untuk menampilkan semua data backend developer
@app.route('/admin/backend', methods=['GET', 'POST'])
@login_required
def admin_backend_route():
    return admin_backend()

# Route untuk menambahkan backend developer baru
@app.route('/admin/backend/add', methods=['GET', 'POST'])
@login_required
def add_backend_route():
    return add_backend()

# Route untuk mengedit backend developer
@app.route('/admin/backend/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_backend_route(id):
    return edit_backend(id)

# Route untuk menghapus backend developer
@app.route('/admin/backend/delete/<int:id>')
@login_required
def delete_backend_route(id):
    return delete_backend(id)




#ROUTE UI UX
# Route untuk menampilkan semua data backend developer
@app.route('/admin/uiux', methods=['GET', 'POST'])
@login_required
def admin_uiux_route():
    return admin_uiux()

# Route untuk menambahkan uiux developer baru
@app.route('/admin/uiux/add', methods=['GET', 'POST'])
@login_required
def add_uiux_route():
    return add_uiux()

# Route untuk mengedit uiux developer
@app.route('/admin/uiux/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_uiux_route(id):
    return edit_uiux(id)

# Route untuk menghapus uiux developer
@app.route('/admin/uiux/delete/<int:id>')
@login_required
def delete_uiux_route(id):
    return delete_uiux(id)



#ROUTE MOBILE
# Route untuk menampilkan semua data backend developer
@app.route('/admin/mobile', methods=['GET', 'POST'])
@login_required
def admin_mobile_route():
    return admin_mobile()

# Route untuk menambahkan mobile developer baru
@app.route('/admin/mobile/add', methods=['GET', 'POST'])
@login_required
def add_mobile_route():
    return add_mobile()

# Route untuk mengedit mobile developer
@app.route('/admin/mobile/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_mobile_route(id):
    return edit_mobile(id)

# Route untuk menghapus mobile developer
@app.route('/admin/mobile/delete/<int:id>')
@login_required
def delete_mobile_route(id):
    return delete_mobile(id)


# Routes Admin Courses populer
@app.route('/admin/courses', methods=['GET', 'POST'])
@login_required
def admin_courses_route():
    return admin_courses()

@app.route('/admin/courses/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_course_route(id):
    return edit_course(id)

@app.route('/admin/courses/delete/<int:id>')
@login_required
def delete_course_route(id):
    return delete_course(id)

# Login & Logout
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)

        user = UserModel.query.filter_by(username=username).first()
        if user and user.password == hashed_password:
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        error = "Username atau password salah!"
    return render_template('admin/login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role == 'admin':
        return render_template('admin/admin.html', user=current_user)
    return "Akses ditolak!"


#ROUTE BE STUDENT

@app.route('/admin/student')
@login_required
def admin_student():
    students = StudentModel.query.all()  # Ambil semua data student dari database
    return render_template('admin/student.html', students=students)  # Render template dengan data

@app.route('/admin/student/edit/<int:id>', methods=['POST'])
def edit_student(id):
    student = StudentModel.query.get_or_404(id)
    student.username = request.form['username']
    student.email = request.form['email']
    student.phone = request.form['phone']


    db.session.commit()
    flash('Student berhasil diperbarui!', 'success')
    return redirect(url_for('admin_student'))


@app.route('/admin/student/delete/<int:id>')
def delete_student(id):
    student = StudentModel.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student berhasil dihapus!', 'success')
    return redirect(url_for('admin_student'))



@app.route('/student/login', methods=['GET', 'POST'])
def login_student():
    return student_login()

@app.route('/student/register', methods=['GET', 'POST'])
def register_student():
    return student_register()

# Routes untuk Student Logout
@app.route('/student/logout')
@login_required
def logout_student():
    return student_logout()

if __name__ == '__main__':
    app.run(debug=True, port=4001)
