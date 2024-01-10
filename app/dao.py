from app.models import Category, Book, UserRoleEnum, Author, Publisher, Customer, DeliveryOfCustomer, DeliveryAddress, PhoneNumber, PersonModel
from app import app, db
import hashlib
from sqlalchemy import func, or_

import cloudinary.uploader


def get_category():
    return Category.query.all()


def count_book():
    return Book.query.count()


# def check_login(username, password):
#     password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
#     return User.query.filter(User.username.__eq__(username.strip()),
#                              User.password.__eq__(password)).first()


def get_book(kw, cate_id, page=None):
    book = Book.query
    if kw:
        book = book.join(Author)
    book = book.join(Publisher)

    if kw:

        book = book.filter(or_(func.lower(Book.BookName).contains(func.lower(kw)),
                               func.lower(Author.FullName).contains(func.lower(kw)),
                               func.lower(Publisher.Publisher_Name).contains(func.lower(kw))))

    if cate_id:
        book = book.filter(Book.Category_ID.__eq__(cate_id))

    if page:
        page = int(page)
        page_size = app.config["PAGE_SIZE"]
        start = (page - 1)*page_size

        return book.slice(start, start + page_size)

    return book.all()


def get_quantity_in_stock(book_id):
    book = Book.query.filter_by(Book_ID=book_id).first()
    return book.QuantityInStock if book else None


def save_customer_info(customer_id, full_name, phone_number, birth_day, address, gender):
    # Kiểm tra xem khách hàng đã tồn tại hay chưa
    existing_customer = Customer.query.filter_by(Customer_ID=customer_id).first()

    if existing_customer:
        # Nếu khách hàng đã tồn tại, kiểm tra xem thông tin có thay đổi không
        if (existing_customer.FullName != full_name or
            existing_customer.BirthDay != birth_day or
            (gender and existing_customer.Gender != gender)):
            # Cập nhật thông tin nếu có thay đổi
            existing_customer.FullName = full_name
            existing_customer.BirthDay = birth_day
            if gender:
                existing_customer.Gender = gender
            # Các bước cập nhật thông tin khác tương tự

        # Kiểm tra xem Số CCCD đã tồn tại chưa
        existing_phone_number = PhoneNumber.query.filter_by(Phone_Number=phone_number, Customer_ID=customer_id).first()
        if not existing_phone_number:
            # Nếu Số CCCD chưa tồn tại, tạo mới và lưu vào CSDL
            new_phone_number = PhoneNumber(Phone_Number=phone_number, Customer_ID=customer_id)
            db.session.add(new_phone_number)

        # Kiểm tra xem địa chỉ giao hàng đã tồn tại chưa
        existing_address = DeliveryAddress.query.filter_by(Address=address).first()
        if not existing_address:
            # Nếu địa chỉ chưa tồn tại, tạo mới và lưu vào CSDL
            new_address = DeliveryAddress(Address=address)
            db.session.add(new_address)

        # Kiểm tra xem thông tin giao hàng của khách hàng đã tồn tại chưa
        existing_delivery_of_customer = DeliveryOfCustomer.query.filter_by(Address_ID=new_address.Address_ID, Customer_ID=customer_id).first()
        if not existing_delivery_of_customer:
            # Nếu thông tin chưa tồn tại, tạo mới và lưu vào CSDL
            new_delivery_of_customer = DeliveryOfCustomer(Address_ID=new_address.Address_ID, Customer_ID=customer_id)
            db.session.add(new_delivery_of_customer)

    else:
        # Nếu khách hàng chưa tồn tại, tạo mới đối tượng Customer và lưu vào CSDL
        new_customer = Customer(Customer_ID=customer_id, FullName=full_name)
        if gender:
            new_customer.Gender = gender
        db.session.add(new_customer)

        # Tạo mới Số CCCD và lưu vào CSDL
        new_phone_number = PhoneNumber(Phone_Number=phone_number, Customer_ID=customer_id)
        db.session.add(new_phone_number)

        # Tạo mới địa chỉ giao hàng và lưu vào CSDL
        new_address = DeliveryAddress(Address=address)
        db.session.add(new_address)

        # Tạo mới thông tin giao hàng của khách hàng và lưu vào CSDL
        new_delivery_of_customer = DeliveryOfCustomer(Address_ID=new_address.Address_ID, Customer_ID=customer_id)
        db.session.add(new_delivery_of_customer)

    db.session.commit()
    return 'Thông tin khách hàng đã được cập nhật.'




