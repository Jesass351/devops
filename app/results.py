from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from models import Result, Competition
from flask_login import login_required, current_user
from bleach import clean

bp = Blueprint('results', __name__, url_prefix='/results')

REVIEW_PARAMS = [
    'horses_to_competitions_id', 'place', 'time'
]

def params():
    return { p: request.form.get(p) for p in REVIEW_PARAMS }

@bp.route('/create_form/<int:competition_id>')
@login_required
def create_form(competition_id):
    # try:
        competition = db.session.execute(db.select(Competition).filter(Competition.id == competition_id)).scalar()
        return render_template('results/create.html', competition=competition)
    # except:
        # flash('Ошибка при отображении формы', 'danger')
        # return redirect(url_for('index'))


@bp.route('/create/<int:competition_id>', methods=['POST'])
@login_required
def create(competition_id):
    # try:
        horses_places = request.form.getlist('horse_place')
        horses_times = request.form.getlist('horse_time')
        horses_ids = request.form.getlist('horse_id')
        horses_to_competitions = request.form.getlist('horses_to_competitions')
        
        print(horses_ids)
        print(horses_places)
        print(horses_times)
        print(horses_to_competitions)
        
        
        
        print('-------------')

        for i in range(len(horses_ids)):
            result = Result(horse_id = horses_ids[i], competition_id=competition_id, place = horses_places[i], time=horses_times[i]) 
            db.session.add(result)
            db.session.commit()
            
        flash('Результаты добавлены', 'success')
        return redirect(url_for('index'))
    # except:
        # flash('Ошибка при создании рецензии', 'danger')
        # return redirect(url_for('reviews.create', book_id = book_id))

        

        


