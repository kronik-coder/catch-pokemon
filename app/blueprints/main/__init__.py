from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix='')

from .import routes

# python -m venv venv
# Windows: venv\scripts\activate
# If the requirements.txt has pkg-resources == 0.0.0 inside of it delete this line and press save (this is something that only works with linux)
# pip install -r requirements.txt
# windows: set FLASK_APP=app.py
# windows: set FLASK_ENV=development
# flask run

# pip install python-dotenv

# pip install flask login
# pip install flask-sqlalchemy flask-migrate psycopg2
# flask db init # initialize a database
# flask db migrate # its like commiting changes into github
# flask db upgrade # like git push