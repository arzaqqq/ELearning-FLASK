from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from models.uiux import UiuxModel
from models import db

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Validasi file gambar
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# List dan tambah frontend
@login_required
def admin_uiux():
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

            new_uiux = UiuxModel(
                title=title,
                image=filename,
                duration=duration,
                price=price
            )
            db.session.add(new_uiux)
            db.session.commit()
            flash('uiux developer berhasil ditambahkan!', 'success')
        else:
            flash('File gambar tidak valid atau tidak dipilih!', 'danger')

    uiuxs = UiuxModel.query.all()
    return render_template('admin/uiux.html', uiuxs=uiuxs)

# Add uiux
@login_required
def add_uiux():
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

            new_uiux = UiuxModel(
                title=title,
                image=filename,
                duration=duration,
                price=price
            )
            db.session.add(new_uiux)
            db.session.commit()
            flash('uiux developer berhasil ditambahkan!', 'success')
            return redirect(url_for('admin_uiux_route'))
        else:
            flash('File gambar tidak valid!', 'danger')

    return render_template('admin/add_uiux.html')

# Edit uiux
@login_required
def edit_uiux(id):
    if current_user.role != 'admin':
        flash("Akses ditolak!", 'danger')
        return redirect(url_for('login'))
    
    uiux = UiuxModel.query.get_or_404(id)
    if request.method == 'POST':
        title = request.form.get('title')
        duration = request.form.get('duration')
        price = request.form.get('price')
        file = request.files.get('image')

        if not title or not duration or not price:
            flash('Semua bidang harus diisi!', 'danger')
        else:
            uiux.title = title
            uiux.duration = duration
            uiux.price = price

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join('static/uploads', filename)
                file.save(filepath)
                uiux.image = filename

            db.session.commit()
            flash('uiux developer berhasil diperbarui!', 'success')
            return redirect(url_for('admin_uiux_route'))

    return render_template('admin/edit_uiux.html', uiux=uiux)

# Hapus uiux
@login_required
def delete_uiux(id):
    if current_user.role != 'admin':
        flash("Akses ditolak!", 'danger')
        return redirect(url_for('login'))
    
    uiux = UiuxModel.query.get_or_404(id)
    db.session.delete(uiux)
    db.session.commit()
    flash('uiux developer berhasil dihapus!', 'success')
    return redirect(url_for('admin_uiux_route'))
