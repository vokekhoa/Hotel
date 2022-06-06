import math
from flask import render_template, request, redirect, url_for, session, jsonify
from hotelapp import app, login
import utils
import cloudinary.uploader
from flask_login import login_user, logout_user
import hotelapp.admin


@app.route("/")
def home():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    page = request.args.get('page', 1)
    rooms = utils.load_rooms(cate_id=cate_id, kw=kw, page=int(page))
    counter = utils.count_rooms()
    return render_template('index.html', rooms=rooms, pages=math.ceil(counter / app.config['PAGE_SIZE']))


@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        avatar_path = None

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                utils.add_user(name=name, username=username, password=password, email=email, avatar=avatar_path)
                return redirect(url_for('user_signin'))
            else:
                err_msg = 'Mật khẩu không khớp!!!'
        except Exception as ex:
            err_msg = 'Lỗi hệ thống!!' + str(ex)

    return render_template('register.html', err_msg=err_msg)


@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect(url_for('home'))
        else:
            err_msg = "Tên đăng nhập hoặc mật khẩu không đúng!!"

    return render_template('login.html', err_msg=err_msg)


@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))


@app.context_processor
def common_response():
    return {
        'categories': utils.load_categories()
    }


@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route("/room")
def room_list():
    cate_id = request.args.get("category_id")
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    rooms = utils.load_rooms(cate_id=cate_id, kw=kw, from_price=from_price, to_price=to_price)
    return render_template('rooms.html', rooms=rooms)


@app.route("/room/<int:room_id>")
def room_detail(room_id):
    room = utils.get_room_by_id(room_id)
    return render_template('rooms_detail.html', room=room)


@app.route('/api/add-cart', methods=['post'])
def add_to_cart():
    id = ''
    name = ''
    price = ''

    cart = session.get('cart')
    if not cart:
        cart = {}
    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'quantity': 1
        }
    session['cart'] = cart
    return jsonify(utils.count_cart(cart))


if __name__ == '__main__':
    from hotelapp.admin import *

    app.run(debug=True)
