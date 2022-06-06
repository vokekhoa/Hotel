import json, os
from hotelapp import app, db
from hotelapp.models import Category, Room, User
import hashlib

def read_json(path):
    with open(path, "r") as f:
        return json.load(f)

def load_categories():
    return Category.query.all()

def load_rooms(cate_id=None, kw=None, from_price=None, to_price=None, page=1):
    rooms = Room.query.filter(Room.active == True)

    if cate_id:
        rooms = rooms.filter(Room.category_id == cate_id)
    if kw:
        rooms = rooms.filter(Room.name.contains(kw))
    if from_price:
        rooms = rooms.filter(Room.price.__ge__(from_price))
    if to_price:
        rooms = rooms.filter(Room.price.__le__(to_price))

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size

    return rooms.slice(start, end).all()


def count_rooms():
    return Room.query.filter(Room.active.__eq__(True)).count()


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(), username=username.strip(), password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar')
                )
    db.session.add(user)
    db.session.commit()


def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_room_by_id(room_id):
    return Room.query.get(room_id)


def count_cart(cart):
    total_quantity, total_amount = 0, 0

    if cart:
        for c in cart.value():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }