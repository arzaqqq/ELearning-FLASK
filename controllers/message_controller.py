from flask import request, redirect, url_for, flash, render_template
from models.message import MessageModel
from models import db

def save_message():
    if request.method == 'POST':
        # Ambil data dari form
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        # Validasi input kosong
        if not name or not email or not subject or not message:
            flash('Semua kolom harus diisi!', 'danger')
            return redirect(url_for('contact'))

        # Simpan ke database
        new_message = MessageModel(name=name, email=email, subject=subject, message=message)
        db.session.add(new_message)
        db.session.commit()

        # Flash message untuk keberhasilan
        flash('Pesan Anda berhasil dikirim! Kami akan segera menghubungi Anda.', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')