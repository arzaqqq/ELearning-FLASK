from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from models.frontend import FrontendModel
from models import db

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Validasi file gambar
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# List dan tambah frontend
@login_required
def admin_frontend():
    if current_user.role != 'admin':
        flash("Akses ditolak!", 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        duration = request.form.get('duration')
        price = request.form.get('price')
        file = request.files.get('image')

        # Validasi input
        if not title or not duration or not price:
            flash('Semua bidang harus diisi!', 'danger')
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join('static/uploads', filename)
            file.save(filepath)

            new_frontend = FrontendModel(
                title=title,
                image=filename,
                duration=duration,
                price=price
            )
            db.session.add(new_frontend)
            db.session.commit()
            flash('Frontend developer berhasil ditambahkan!', 'success')
        else:
            flash('File gambar tidak valid atau tidak dipilih!', 'danger')

    frontends = FrontendModel.query.all()
    return render_template('admin/frontend.html', frontends=frontends)

# Add frontend
@login_required
def add_frontend():
    if current_user.role != 'admin':
        flash("Akses ditolak!", 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        duration = request.form.get('duration')
        price = request.form.get('price')
        file = request.files.get('image')

        if not title or not duration or not price:
            flash('Semua bidang harus diisi!', 'danger')
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join('static/uploads', filename)
            file.save(filepath)

            new_frontend = FrontendModel(
                title=title,
                image=filename,
                duration=duration,
                price=price
            )
            db.session.add(new_frontend)
            db.session.commit()
            flash('Frontend developer berhasil ditambahkan!', 'success')
            return redirect(url_for('admin_frontend_route'))
        else:
            flash('File gambar tidak valid!', 'danger')

    return render_template('admin/add_frontend.html')

# Edit frontend
@login_required
def edit_frontend(id):
    if current_user.role != 'admin':
        flash("Akses ditolak!", 'danger')
        return redirect(url_for('login'))
    
    frontend = FrontendModel.query.get_or_404(id)
    if request.method == 'POST':
        title = request.form.get('title')
        duration = request.form.get('duration')
        price = request.form.get('price')
        file = request.files.get('image')

        if not title or not duration or not price:
            flash('Semua bidang harus diisi!', 'danger')
        else:
            frontend.title = title
            frontend.duration = duration
            frontend.price = price

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join('static/uploads', filename)
                file.save(filepath)
                frontend.image = filename

            db.session.commit()
            flash('Frontend developer berhasil diperbarui!', 'success')
            return redirect(url_for('admin_frontend_route'))

    return render_template('admin/edit_frontend.html', frontend=frontend)

# Hapus frontend
@login_required
def delete_frontend(id):
    if current_user.role != 'admin':
        flash("Akses ditolak!", 'danger')
        return redirect(url_for('login'))
    
    frontend = FrontendModel.query.get_or_404(id)
    db.session.delete(frontend)
    db.session.commit()
    flash('Frontend developer berhasil dihapus!', 'success')
    return redirect(url_for('admin_frontend_route'))
