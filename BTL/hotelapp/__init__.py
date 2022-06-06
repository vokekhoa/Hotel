from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:khoavo00@localhost/hotelapp?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key ='$&(^(&7658789GJGYSKDUC'
app.config['PAGE_SIZE'] = 8

db = SQLAlchemy(app=app)

admin = Admin(app=app, name='TEYVAT HOTEL', template_mode='bootstrap4')

cloudinary.config(
    cloud_name='dd7ggpbgg',
    api_key='752959888913966',
    api_secret='_Zq4ZScD2wyjldCwUk88c6cKvcg'
)


login = LoginManager(app=app)