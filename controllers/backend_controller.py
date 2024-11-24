from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from models.backend import BackendModel
from models import db

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Validasi file gambar
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# List dan tambah backend
@login_required
def admin_backend():
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

            new_backend = BackendModel(
                title=title,
                image=filename,
                duration=duration,
                price=price
            )
            db.session.add(new_backend)
            db.session.commit()
            flash('backend developer berhasil ditambahkan!', 'success')
        else:
            flash('File gambar tidak valid atau tidak dipilih!', 'danger')

    backends = BackendModel.query.all()
    return render_template('admin/backend.html', backends=backends)

# Add backend
@login_required
def add_backend():
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

            new_backend = BackendModel(
                title=title,
                image=filename,
                duration=duration,
                price=price
            )
            db.session.add(new_backend)
            db.session.commit()
            flash('backend developer berhasil ditambahkan!', 'success')
            return redirect(url_for('admin_backend_route'))
        else:
            flash('File gambar tidak valid!', 'danger')

    return render_template('admin/add_backend.html')

# Edit backend
@login_required
def edit_backend(id):
    if current_user.role != 'admin':
        flash("Akses ditolak!", 'danger')
        return redirect(url_for('login'))
    
    backend = BackendModel.query.get_or_404(id)
    if request.method == 'POST':
        title = request.form.get('title')
        duration = request.form.get('duration')
        price = request.form.get('price')
        file = request.files.get('image')

        if not title or not duration or not price:
            flash('Semua bidang harus diisi!', 'danger')
        else:
            backend.title = title
            backend.duration = duration
            backend.price = price

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join('static/uploads', filename)
                file.save(filepath)
                backend.image = filename

            db.session.commit()
            flash('backend developer berhasil diperbarui!', 'success')
            return redirect(url_for('admin_backend_route'))

    return render_template('admin/edit_backend.html', backend=backend)

# Hapus backend
@login_required
def delete_backend(id):
    if current_user.role != 'admin':
        flash("Akses ditolak!", 'danger')
        return redirect(url_for('login'))
    
    backend = BackendModel.query.get_or_404(id)
    db.session.delete(backend)
    db.session.commit()
    flash('backend developer berhasil dihapus!', 'success')
    return redirect(url_for('admin_backend_route'))
