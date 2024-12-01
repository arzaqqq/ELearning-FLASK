from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.student import StudentModel
from models import db
from flask import session


from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


# Fungsi untuk Registrasi Student
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
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('login_student'))  # Arahkan ke halaman login setelah registrasi berhasil

    # Render template jika metode GET
    return render_template('register.html')

# Fungsi untuk Login Student


def student_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        student = StudentModel.query.filter_by(username=username).first()

        if not student or not student.check_password(password):
            flash('Username atau password salah!', 'danger')
            return redirect(url_for('login_student'))

        login_user(student)  # Call login_user after validation
        session.modified = True  # Force session update
        flash('Login berhasil!', 'success')

        # Periksa apakah role benar-benar 'student' setelah login
        if student.role == 'student':
            return redirect(url_for('home'))  # Redirect to home
        else:
            flash('Akses hanya untuk student!', 'danger')
            return redirect(url_for('login_student'))

    return render_template('login.html')



# Fungsi untuk Logout Student
@login_required
def student_logout():
    logout_user()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('login_student'))

