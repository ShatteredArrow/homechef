from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from os.path import join, dirname, realpath



UPLOAD_FOLDER = join(dirname(realpath(__file__)), *['static', 'recipe_images'])
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['IMGUR_UPLOAD_ULR'] = "https://api.imgur.com/3/image"


db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)



from app import routes, models


