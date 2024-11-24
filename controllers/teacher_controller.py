from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from models.teacher import TeacherModel
from models import db

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Validasi file gambar
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# List dan tambah teacher
@login_required
def admin_teacher():
    if current_user.role != 'admin':
        return "Akses ditolak!"
    
    if request.method == 'POST':
        name = request.form['name']
        expertise = request.form['expertise']
        linkedin = request.form['linkedin']
        facebook = request.form['facebook']
        instagram = request.form['instagram']
        file = request.files['image']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join('static/uploads', filename)
            file.save(filepath)

            new_teacher = TeacherModel(
                name=name,
                expertise=expertise,
                image=filename,
                linkedin=linkedin,
                facebook=facebook,
                instagram=instagram
            )
            db.session.add(new_teacher)
            db.session.commit()
            flash('Teacher added successfully!', 'success')
        else:
            flash('Invalid image file!', 'danger')

    teachers = TeacherModel.query.all()
    return render_template('admin/teacher.html', teachers=teachers)

# Edit teacher
@login_required
def edit_teacher(id):
    if current_user.role != 'admin':
        return "Akses ditolak!"
    
    teacher = TeacherModel.query.get_or_404(id)
    if request.method == 'POST':
        teacher.name = request.form['name']
        teacher.expertise = request.form['expertise']
        teacher.linkedin = request.form['linkedin']
        teacher.facebook = request.form['facebook']
        teacher.instagram = request.form['instagram']

        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join('static/uploads', filename)
            file.save(filepath)
            teacher.image = filename

        db.session.commit()
        flash('Teacher updated successfully!', 'success')
        return redirect(url_for('admin_teacher_route'))

    return render_template('admin/edit_teacher.html', teacher=teacher)

# Hapus teacher
@login_required
def delete_teacher(id):
    if current_user.role != 'admin':
        return "Akses ditolak!"
    
    teacher = TeacherModel.query.get_or_404(id)
    db.session.delete(teacher)
    db.session.commit()
    flash('Teacher deleted successfully!', 'success')
    return redirect(url_for('admin_teacher_route'))
