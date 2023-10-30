from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from models import Horse, Jokey, Gender, Owner, Result
from flask_login import login_required, current_user
from bleach import clean

bp = Blueprint('staff', __name__, url_prefix='/staff')

@bp.route('horses', methods=['POST', 'GET'])
def horses():
    if request.method == 'GET':
        horses = db.session.execute(db.select(Horse)).scalars()
        return render_template('staff/horses.html', horses=horses)
    if request.method == 'POST':
        horse_id = request.form.get('horse_id')
        horses = db.session.execute(db.select(Horse)).scalars()
        
        selected_horse = db.session.execute(db.select(Horse).filter(Horse.id == horse_id)).scalar()
        return render_template('staff/horses.html', selected_horse=selected_horse, horses=horses)

@bp.route('jokeys', methods=['POST', 'GET'])
def jokeys():
    if request.method == 'GET':
        jokeys = db.session.execute(db.select(Jokey)).scalars()
        return render_template('staff/jokeys.html', jokeys=jokeys)
    
    if request.method == 'POST':
        jokey_id = request.form.get('jokey_id')
        jokeys = db.session.execute(db.select(Jokey)).scalars()

        selected_jokey = db.session.execute(db.select(Jokey).filter(Jokey.id == jokey_id)).scalar()
        return render_template('staff/jokeys.html', selected_jokey=selected_jokey, jokeys=jokeys)

@bp.route('/create_horse', methods=['GET', 'POST'])
@login_required
def create_horse():
    if request.method == 'GET':
        genders = db.session.execute(db.select(Gender)).scalars()
        owners = db.session.execute(db.select(Owner)).scalars()
        jokeys = db.session.execute(db.select(Jokey)).scalars()
        
        return render_template('staff/create_horse.html', genders=genders, owners=owners, jokeys=jokeys)
    if request.method == 'POST':
        name = request.form.get('name')
        gender_id = request.form.get('gender')
        age = request.form.get('age')
        jokey_id = request.form.get('jokey')
        owner_id = request.form.get('owner')
        horse = Horse(name=name, gender_id=gender_id, age=age,
                      jokey_id=jokey_id, owner_id=owner_id)
        
        db.session.add(horse)
        db.session.commit()
        
        return redirect(url_for('index'))
        
    # except:
        # flash('Ошибка при отображении формы', 'danger')
        # return redirect(url_for('index'))
        
@bp.route('/create_owner', methods=['GET', 'POST'])
@login_required
def create_owner():
    if request.method == 'GET':
        return render_template('staff/create_owner.html')
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        
        owner = Owner(name=name, address=address, phone=phone)
        db.session.add(owner)
        db.session.commit()
        return redirect(url_for('index'))
    # except:
        # flash('Ошибка при отображении формы', 'danger')
        # return redirect(url_for('index'))

@bp.route('/create_jokey', methods=['GET', 'POST'])
@login_required
def create_jokey():
    if request.method == 'GET':
        return render_template('staff/create_jokey.html')
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        rating = request.form.get('rating')
        age = request.form.get('age')
        
        
        jokey = Jokey(name=name, address=address, rating=rating,age=age )
        db.session.add(jokey)
        db.session.commit()
        return redirect(url_for('index'))
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
            result = Result(horses_to_competitions_id = horses_to_competitions[i], place = horses_places[i], time=horses_times[i]) 
            db.session.add(result)
            db.session.commit()
            
            results_competitions = Result_To_Competition(result_id = result.id, competition_id = competition_id)
            db.session.add(results_competitions)
            db.session.commit()
        flash('Рецензия добавлена', 'success')
        return redirect(url_for('books.detailed', book_id=book_id))
    # except:
        # flash('Ошибка при создании рецензии', 'danger')
        # return redirect(url_for('reviews.create', book_id = book_id))

        

        


