from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/home')
def homepage():
    return render_template("index.html", user=current_user)

@views.route('/top')
def top():
    return render_template("top.html", user=current_user)

@views.route('/bottom')
def bottom():
    return render_template("bottom.html", user=current_user)

@views.route('/lingeries')
def lingeries():
    return render_template("lingeries.html", user=current_user)

@views.route('/jackets')
def jackets():
    return render_template("jackets.html", user=current_user)

@views.route('/shoes')
def shoes():
    return render_template("shoes.html", user=current_user)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})