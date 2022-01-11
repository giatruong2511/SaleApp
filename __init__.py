from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = 'dkfsakADFLFFJ343534JDR343W@243435312!$!4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1951050100@localhost/ttth?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK-MODIFICATIONS'] = True

db = SQLAlchemy(app = app)
login = LoginManager(app=app)
