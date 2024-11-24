from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from models.mobile import MobileModel
from models import db

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Validasi file gambar
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# List dan tambah frontend
@login_required
def admin_mobile():
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

            new_mobile = MobileModel(
                title=title,
                image=filename,
                duration=duration,
                price=price
            )
            db.session.add(new_mobile)
            db.session.commit()
            flash('mobile developer berhasil ditambahkan!', 'success')
        else:
            flash('File gambar tidak valid atau tidak dipilih!', 'danger')

    mobiles = MobileModel.query.all()
    return render_template('admin/mobile.html', mobiles=mobiles)

# Add mobile
@login_required
def add_mobile():
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

            new_mobile = MobileModel(
                title=title,
                image=filename,
                duration=duration,
                price=price
            )
            db.session.add(new_mobile)
            db.session.commit()
            flash('mobile developer berhasil ditambahkan!', 'success')
            return redirect(url_for('admin_mobile_route'))
        else:
            flash('File gambar tidak valid!', 'danger')

    return render_template('admin/add_mobile.html')

# Edit mobile
@login_required
def edit_mobile(id):
    if current_user.role != 'admin':
        flash("Akses ditolak!", 'danger')
        return redirect(url_for('login'))
    
    mobile = MobileModel.query.get_or_404(id)
    if request.method == 'POST':
        title = request.form.get('title')
        duration = request.form.get('duration')
        price = request.form.get('price')
        file = request.files.get('image')

        if not title or not duration or not price:
            flash('Semua bidang harus diisi!', 'danger')
        else:
            mobile.title = title
            mobile.duration = duration
            mobile.price = price

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join('static/uploads', filename)
                file.save(filepath)
                mobile.image = filename

            db.session.commit()
            flash('mobile developer berhasil diperbarui!', 'success')
            return redirect(url_for('admin_mobile_route'))

    return render_template('admin/edit_mobile.html', mobile=mobile)

# Hapus mobile
@login_required
def delete_mobile(id):
    if current_user.role != 'admin':
        flash("Akses ditolak!", 'danger')
        return redirect(url_for('login'))
    
    mobile = MobileModel.query.get_or_404(id)
    db.session.delete(mobile)
    db.session.commit()
    flash('mobile developer berhasil dihapus!', 'success')
    return redirect(url_for('admin_mobile_route'))
