from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from models import Horse, Jokey, Gender, Owner, Result
from flask_login import login_required, current_user
from bleach import clean
from prometheus_client import generate_latest
from prometheus_client import Counter

bp = Blueprint('staff', __name__, url_prefix='/staff')
c = Counter('requests_for_horses', 'Number of runs of the process_request method', ['method', 'endpoint'])


@bp.route('horses', methods=['POST', 'GET'])
def horses():
    if request.method == 'GET':
        path = str(request.path)
        verb = request.method
        label_dict = {"method": verb, "endpoint": path}
        c.labels(**label_dict).inc()
    
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
        flash('Лошадь успешно добавлена','success')
        
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
        flash('Владелец успешно добавлен','success')
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
        flash('Жокей успешно добавлен','success')
        return redirect(url_for('index'))
    # except:
        # flash('Ошибка при отображении формы', 'danger')
        # return redirect(url_for('index'))

        

        


