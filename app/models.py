import os
import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask import url_for
from app import db, app
from users_policy import UsersPolicy
from sqlalchemy.sql import func

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.Text, nullable=False)
    test = db.Column(db.Text)
    

    def __repr__(self):
        return '<Role %r>' % self.title

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def is_administrator(self):
        return self.role_id == app.config['ADMINISTRATOR_ROLE']
    
    @property
    def is_moderator(self):
        return self.role_id == app.config['MODERATOR_ROLE']
    
    def can(self, action, record=None):
        users_policy = UsersPolicy(record)
        method = getattr(users_policy, action, None)
        if method:
            return method()
        return False

    @property
    def full_name(self):
        return ' '.join([self.last_name, self.first_name, self.middle_name or ''])

    def __repr__(self):
        return '<User %r>' % self.login
    
class Gender(db.Model):
    __tablename__ = 'genders'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

class Owner(db.Model):
    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    
    def __repr__(self):
        return '<Jokey %r>' % self.name

class Jokey(db.Model):
    __tablename__ = 'jokeys'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    
    @property
    def horses(self):
        return db.session.execute(db.select(Horse).filter(Horse.jokey_id == self.id)).scalars()

    
    def __repr__(self):
        return '<Jokey %r>' % self.name

class Horse(db.Model):
    __tablename__ = 'horses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender_id = db.Column(db.Integer,  db.ForeignKey('genders.id'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    jokey_id = db.Column(db.Integer,  db.ForeignKey('jokeys.id'), nullable=False)
    owner_id = db.Column(db.Integer,  db.ForeignKey('owners.id'), nullable=False)
    
    @property
    def horses_to_competitions(self):
        return db.session.execute(db.select(Horse_To_Competition).filter(Horse_To_Competition.horse_id == self.id)).scalar()
    
    @property
    def gender(self):
        return db.session.execute(db.select(Gender).filter_by(id=self.gender_id)).scalar()
    
    @property
    def jokey(self):
        return db.session.execute(db.select(Jokey).filter_by(id=self.jokey_id)).scalar()
    
    @property
    def owner(self):
        return db.session.execute(db.select(Owner).filter_by(id=self.owner_id)).scalar()
    
    @property
    def competitions(self):
        horses_to_competitions = db.session.execute(db.select(Horse_To_Competition).filter(Horse_To_Competition.horse_id == self.id)).scalars()
        results = []
        
        for horse_competition in horses_to_competitions:
            result = db.session.execute(db.select(Competition).filter(Competition.id == horse_competition.competition_id)).scalar()
            results.append(result)
            
        return results
    
    def __repr__(self):
        return '<Horse %r>' % self.name

class Competition(db.Model):
    __tablename__ = 'competitions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    
    @property
    def horses(self):
        competitions_horses = db.session.execute(db.Select(Horse_To_Competition).filter_by(competition_id = self.id)).all()
        horses = []
        for competition_horse in competitions_horses:
            horse = db.session.execute(db.select(Horse).filter(Horse.id == competition_horse[0].horse_id)).scalar()
            horses.append(horse)
        return horses
    
    @property
    def result(self):
        results = db.session.execute(db.select(Result).filter(Result.competition_id == self.id)).scalars()
        return_array = []
        for result in results:
            horse = db.session.execute(db.select(Horse).filter(Horse.id == result.horse_id)).scalar()
            jokey = db.session.execute(db.select(Jokey).filter(Jokey.id == horse.jokey_id)).scalar()
            owner = db.session.execute(db.select(Owner).filter(Owner.id == horse.owner_id)).scalar()
            
            
            final_result = {
                'horse': horse,
                'place': result.place,
                'time': result.time,
                'jokey': jokey,
                'owner': owner,
            }
            return_array.append(final_result)
        return return_array
    
    def info_about_horse(self, horse_id):
        info = db.session.execute(db.select(Result).filter(
            Result.competition_id == self.id,
            Result.horse_id == horse_id
            )).scalar()
        return info
    
    def __repr__(self):
        return '<Competition %r>' % self.title
    
class Horse_To_Competition(db.Model):
    __tablename__ = 'horses_to_competitions'
    id = db.Column(db.Integer, primary_key=True)
    horse_id = db.Column(db.Integer,  db.ForeignKey('horses.id'), nullable=False)
    competition_id = db.Column(db.Integer,  db.ForeignKey('competitions.id'), nullable=False) 
    
class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    horse_id = db.Column(db.Integer,  db.ForeignKey('horses.id'), nullable=False)
    competition_id = db.Column(db.Integer,  db.ForeignKey('competitions.id'), nullable=False)
    place = db.Column(db.Integer, nullable=False)
    time = db.Column(db.String(100), nullable=False)
    
    
    