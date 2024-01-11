import math
from flask import render_template, request, redirect, jsonify, session
import dao
import utils
from app import app, login
from flask_login import login_user, logout_user
from flask import flash
from flask import render_template, request, jsonify, session, redirect

import dao
import utils
from app import app


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


@app.route('/api/check_quantity', methods=['post'])
def check_quantity():
    data = request.json
    book_id = str(data.get("Book_ID"))
    quantity_in_stock = dao.get_quantity_in_stock(book_id)
    return jsonify({"quantity_in_took": quantity_in_stock})


@app.route('/api/cart', methods=['post'])
def add_to_cart():
    """
    {
        "1": {
            "id": "1",
            "name": "abc",
            "price": 123,
            "quantity": 2
        }, "2": {
            "id": "2",
            "name": "abc",
            "price": 123,
            "quantity": 1
        }
    }
    """

    cart = session.get('cart')
    if cart is None:
        cart = {}

    data = request.json
    book_id = str(data.get("Book_ID"))
    quantity = data.get("quantity")

    quantity_in_stock = dao.get_quantity_in_stock(book_id)
    if quantity_in_stock is not None and quantity > quantity_in_stock:
        return jsonify({"success": False, "error": "Sản phẩm đã hết hàng."})

    if quantity_in_stock is not None and book_id in cart:
        total_quantity_in_cart = cart[book_id]['quantity'] + quantity
        if total_quantity_in_cart > quantity_in_stock:
            return jsonify({"success": False, "error": "Sản phẩm không đủ hàng trong kho."})
    if book_id in cart:
            cart[book_id]['quantity'] += 1
    else:
        cart[book_id] = {
            "Book_ID": book_id,
            "BookName": data.get("BookName"),
            "Price": data.get("Price"),
            "quantity": 1
        }

    session['cart'] = cart
    return jsonify({"success": True, "message": "Sản phẩm đã được thêm vào giỏ hàng.", "cart": utils.count_cart(cart)})


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


@app.route('/info', methods=['get', 'post'])
def save_customer_info_route():
    err_msg = None
    if request.method.__eq__('POST'):
        customer_id = request.form.get('Customer_ID')
        full_name = request.form.get('FullName')
        gender = request.form.get('Gender')
        phone_number = request.form.get('Phone_Number')
        birth_day = request.form.get('BirthDay')
        address = request.form.get('Address')
        if all([customer_id, full_name, gender, phone_number, birth_day, address]):
            try:
                dao.save_customer_info(customer_id=request.form.get('Customer_ID'),
                                       full_name=request.form.get('FullName'),
                                       gender=request.form.get('Gender'),
                                       phone_number=request.form.get('Phone_Number'),
                                       birth_day=request.form.get('BirthDay'),
                                       address=request.form.get('Address'))
            except Exception as ex:
                err_msg = str(ex)
            else:
                return redirect('/cart')
        else:
            err_msg = "Nhập thông tin đầy đủ "

    return render_template('info.html', err_msg=err_msg)


@app.context_processor
def common_responses():
    return {
        'categories': dao.get_category(),
        'cart_stats': utils.count_cart(session.get('cart'))
    }


# @app.route('/user-login', methods=['get', 'post'])
# def user_signin():
#     if request.method.__eq__('POST'):
#         username = request.form.get('username')
#         password = request.form.get('password')
#     return render_template('login.html')


if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
