import math
from flask import render_template, request, redirect, jsonify, session
import dao
import utils
from app import app, login
from flask_login import login_user, logout_user
from flask import flash
from flask import render_template, request, jsonify, session, redirect, url_for
from app.models import Category, Book, UserRoleEnum, Author, Publisher, Customer, DeliveryOfCustomer, DeliveryAddress, PhoneNumber, PersonModel
import dao
from datetime import datetime
import utils
from app import app, db


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
def cart_route():
    save_status = request.args.get('save_status')

    # Kiểm tra nếu trạng thái lưu là 'success'
    if save_status == 'success':
        # Nếu 'save_status' là 'success', đặt biến session để chỉ định điều đó
        session['save_status'] = 'success'

    return render_template('cart.html', save_status=save_status,
                           delivery_method=session.get('delivery_method'),
                           customer_id=session.get('customer_id'))


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


@app.route('/info', methods=['GET', 'POST'])
def save_customer_info_route():
    if request.method == 'POST':
        try:
            customer_id = request.form.get('Customer_ID')
            full_name = request.form.get('FullName')
            gender = request.form.get('Gender')
            phone_number_str = request.form.get('Phone_Number')
            birth_day_str = request.form.get('BirthDay')
            address = request.form.get('Address')

            app.logger.info(
                f"Received data: {customer_id}, {full_name}, {gender}, {phone_number_str}, {birth_day_str}, {address}")

            delivery_method = request.form.get('deliveryMethod')

            session['delivery_method'] = delivery_method
            session['customer_id'] = customer_id

            print("Giá trị của delivery_method và customer_id:", session.get('delivery_method'),
                  session.get('customer_id'))

            if all([customer_id, full_name, gender, phone_number_str, birth_day_str, address]):
                # Chuyển đổi kiểu dữ liệu cho phù hợp với thuộc tính
                phone_number = PhoneNumber(Phone_Number=phone_number_str)
                birth_day = datetime.strptime(birth_day_str, '%Y-%m-%d').date()

                # Chuyển đổi full_name, gender, và address thành định dạng chữ cái đầu viết hoa và các chữ sau viết thường
                full_name = full_name.title()
                gender = gender.title()
                address = address.title()

                # Tạo đối tượng customer
                customer = Customer(
                    Customer_ID=customer_id,
                    FullName=full_name,
                    Gender=gender,
                    phone_number=[phone_number],  # Sử dụng 1 đối tượng phone number duy nhất
                    BirthDay=birth_day,
                )

                db.session.add(customer)

                # Tạo ra đối tượng DeliveryAddress
                delivery_address = DeliveryAddress(Address=address)
                db.session.add(delivery_address)

                # Tạo ra đối tượng DeliveryOfCustomer và liên kết với Customer và DeliveryAddress
                delivery_of_customer = DeliveryOfCustomer(
                    customer=customer,
                    address=delivery_address
                )

                db.session.add(delivery_of_customer)

                # Lưu thay đổi vào CSDL
                db.session.commit()

                app.logger.info("Dữ liệu được lưu thành công")
                flash('success', 'save_status')
                # Redirect to '/cart' with save_status parameter
                return redirect(url_for('cart_route', save_status='success'))
            else:
                app.logger.warning("Dữ liệu không hợp lệ")
                flash('error', 'save_status')
                return "Lưu không thành công"
        except Exception as e:
            app.logger.error(f"Lỗi khi lưu dữ liệu: {e}")
            flash('error', 'save_status')
            return "Lưu không thành công"

    else:
        # Xóa 'save_status' khi truy cập trang '/info'
        session.pop('save_status', None)

    return render_template('info.html')


@app.route('/api/pay', methods=['post'])
def pay():
    cart = session.get('cart')
    delivery_method = session.get('delivery_method')
    customer_id = session.get('customer_id')
    if dao.add_bill(cart, delivery_method, customer_id):
        session.pop('cart', None)
        session.pop('delivery_method', None)
        session.pop('customer_id', None)
        return jsonify({'status': 200})

    return jsonify({'status': 500, 'err_msg': 'Somsthing wrong!'})


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
