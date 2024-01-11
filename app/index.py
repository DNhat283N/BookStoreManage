import math
from flask import render_template, request, redirect, jsonify, session
import dao
import utils
from app import app, login
from flask_login import login_user, logout_user


@app.route('/')
def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    page = request.args.get('page')

    num = dao.count_book()
    page_size = app.config["PAGE_SIZE"]

    pro = dao.get_book(kw, cate_id, page)
    return render_template('index.html', pages=math.ceil(num / page_size), produces=pro)


@app.route('/admin/login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.authenticated_login(username=username, password=password)
    if user:
        login_user(user)
    return redirect('/admin')


@login.user_loader
def load_account(account_id):
    return dao.get_user_by_id(account_id)


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/api/cart', methods=['post'])
def add_to_cart():
    '''
    {
        "cart": {
            "1": {
                "Book_ID": "1",
                "BookName": "ABC",
                "Price": 123,
                "quantity": 2
            },
            "2": {
                "Book_ID": "2",
                "BookName": "ABC",
                "Price": 123,
                "quantity": 1
            }
        }
    }
    '''

    cart = session.get('cart')
    if cart is None:
        cart = {}

    data = request.json
    id = str(data.get("Book_ID"))

    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            "Book_ID": id,
            "BookName": data.get("BookName"),
            "Price": data.get("Price"),
            "quantity": 1
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/cart/<ID_Book>', methods=['put'])
def update_product(ID_Book):
    cart = session.get('cart')
    if cart and ID_Book in cart:
        quantity = request.json.get('quantity')
        cart[ID_Book]['quantity'] = int(quantity)

    session['cart'] = cart
    return jsonify(utils.count_cart(cart))


@app.route('/api/cart/<ID_Book>', methods=['delete'])
def delete_product(ID_Book):
    cart = session.get('cart')
    if cart and ID_Book in cart:
        del cart[ID_Book]

    session['cart'] = cart
    return jsonify(utils.count_cart(cart))


@app.context_processor
def common_responses():
    return {
        'categories': dao.get_category(),
        'cart_stats': utils.count_cart(session.get('cart'))
    }


if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
