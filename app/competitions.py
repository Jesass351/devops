from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db, app
from models import Competition, Horse, Horse_To_Competition
from flask_login import login_required
from auth import check_rights
from bleach import clean

import os

bp = Blueprint('competitions', __name__, url_prefix='/competitions')

BOOK_PARAMS = [
    'id', 'title', 'date', 'place'
]

def params():
    return { p: request.form.get(p) for p in BOOK_PARAMS }

@bp.route('/create_form')
@login_required
@check_rights('book_create')
def create_form():
    try:
        horses = db.session.execute(db.select(Horse)).scalars()
        return render_template('competitions/create.html',horses=horses)
    except:
        flash('Ошибка отображения формы', 'danger')
        return redirect(url_for('index'))

@bp.route('/create', methods=['POST'])
@login_required
@check_rights('book_create')
def create():
    # try:
        
        params_from_form = params()
        for param in params_from_form:
            param = clean(param)
              
        competition = Competition(**params_from_form)

        db.session.add(competition)
        db.session.commit()
        
        horses = request.form.getlist("horses")

        for horse in horses:
            db.session.add(Horse_To_Competition(horse_id = horse,competition_id = competition.id))
        db.session.commit()

        return redirect(url_for('index'))
    # except:
        # db.session.rollback()
        # flash('Ошибка при добавлении', 'danger')
        # return redirect(url_for('books.create'))



        



