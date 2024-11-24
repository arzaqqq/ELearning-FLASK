from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from models.course import CourseModel
from models import db

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Validasi file gambar
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# List dan tambah course
@login_required
def admin_courses():
    if current_user.role != 'admin':
        return "Akses ditolak!"
    
    if request.method == 'POST':
        title = request.form['title']
        duration = request.form['duration']
        price = request.form['price']
        file = request.files['image']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join('static/uploads', filename)
            file.save(filepath)

            new_course = CourseModel(
                title=title,
                image=filename,
                duration=duration,
                price=price
            )
            db.session.add(new_course)
            db.session.commit()
            flash('Course added successfully!', 'success')
        else:
            flash('Invalid image file!', 'danger')

    courses = CourseModel.query.all()
    return render_template('admin/courses_populer.html', courses=courses)

# Edit course
@login_required
def edit_course(id):
    if current_user.role != 'admin':
        return "Akses ditolak!"
    
    course = CourseModel.query.get_or_404(id)
    if request.method == 'POST':
        course.title = request.form['title']
        course.duration = request.form['duration']
        course.price = request.form['price']

        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join('static/uploads', filename)
            file.save(filepath)
            course.image = filename

        db.session.commit()
        flash('Course updated successfully!', 'success')
        return redirect(url_for('admin_courses_route'))

    return render_template('admin/edit_course.html', course=course)

# Hapus course
@login_required
def delete_course(id):
    if current_user.role != 'admin':
        return "Akses ditolak!"
    
    course = CourseModel.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted successfully!', 'success')
    return redirect(url_for('admin_courses_route'))
