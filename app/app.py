from flask import Flask, render_template, request, send_from_directory, flash
from sqlalchemy import MetaData, func
from flask_sqlalchemy import SQLAlchemy
from math import ceil
from flask_migrate import Migrate

from prometheus_client import generate_latest
from prometheus_client import Counter
from prometheus_client import Summary

app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')

INDEX_TIME = Summary('index_request_processing_seconds', 'DESC: INDEX time spent processing request')

c = Counter('requests_for_host', 'Number of runs of the process_request method', ['method', 'endpoint'])

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

from models import *

from auth import bp as auth_bp, init_login_manager
from competitions import bp as competitions_bp
from results import bp as results_bp
from staff import bp as staff_bp


app.register_blueprint(auth_bp)
app.register_blueprint(competitions_bp)
app.register_blueprint(results_bp)
app.register_blueprint(staff_bp)


init_login_manager(app)


# from models import Book, Cove
@app.route('/')
@INDEX_TIME.time()
def index():
    # try:
        current_page = request.args.get('page', 1, type=int)
        books_offset = app.config['BOOKS_ON_INDEX_PAGE'] * (current_page - 1)
        
        competitions = db.session.execute(db.select(Competition).limit(app.config['BOOKS_ON_INDEX_PAGE']).offset(books_offset)).scalars()
        competitions_count = db.session.query(func.count(Competition.id)).scalar()
        pages = ceil(competitions_count / app.config['BOOKS_ON_INDEX_PAGE'])
        path = str(request.path)
        verb = request.method
        label_dict = {"method": verb, "endpoint": path}
        c.labels(**label_dict).inc()
        if pages == 0:
            pages = 1
        
        return render_template(
            'index.html',
            competitions = competitions,
            page = current_page,
            page_count = pages
        )
    # except:
    #     flash("Ошибка при загрузке",'danger')
    #     return render_template(
    #     'index.html',
    #     books = [],
    #     page = 1,
    #     pages = 1
    #     )

def cover(cover_id):
    img = db.get_or_404(Cover, cover_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               img.storage_filename)
                               
@app.route('/metrics')
def metrics():
    return generate_latest()
                              
