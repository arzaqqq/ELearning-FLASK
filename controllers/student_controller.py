from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.student import StudentModel
from models import db



def student_register():
    if request.method == 'POST':
        # Ambil data dari form
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        # Validasi input kosong
        if not username or not email or not phone or not password:
            flash('Semua data harus diisi!', 'danger')
            return redirect(url_for('register_student'))

        # Hash password
        hashed_password = StudentModel.hash_password(password)

        # Cek apakah username, email, atau nomor HP sudah terdaftar
        existing_user = StudentModel.query.filter(
            (StudentModel.username == username) |
            (StudentModel.email == email) |
            (StudentModel.phone == phone)
        ).first()
        if existing_user:
            flash('Username, email, atau nomor HP sudah terdaftar!', 'danger')
            return redirect(url_for('register_student'))

        # Buat user baru
        student = StudentModel(username=username, email=email, phone=phone, password=hashed_password)
        db.session.add(student)
        db.session.commit()

        # Flash message untuk berhasil
        flash('Registrasi berhasil! Anda akan diarahkan ke halaman login.', 'success')
        return redirect(url_for('register_student'))  # Tetap di halaman register untuk JavaScript redirect

    # Render template jika metode GET
    return render_template('register.html')


def student_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Cari user berdasarkan username
        student = StudentModel.query.filter_by(username=username).first()
        if student and student.check_password(password):
            login_user(student)
            flash('Login berhasil!', 'success')
            return redirect(url_for('home'))

        # Flash message untuk login gagal
        flash('Username atau password salah!', 'danger')
        return redirect(url_for('login_student'))

    return render_template('login.html')


@login_required
def student_logout():
    logout_user()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('login_student'))
