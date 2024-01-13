from app.models import Category, Book, Customer, Bill, BillDetail, Author, Publisher
from app import app, db
from sqlalchemy import func, or_, desc
from flask import session

import hashlib
from datetime import datetime


def get_category():
    return Category.query.all()


def count_book():
    return Book.query.count()


def authenticated_login(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    return Account.query.filter(Account.Username.__eq__(username),
                                Account.Password.__eq__(password)).first()


def get_book(kw, cate_id, page=None):
    book = Book.query
    if kw:
        book = book.join(Author)
        book = book.join(Publisher)

    if kw:
        book = book.filter(or_(func.lower(Book.BookName).contains(func.lower(kw)),
                               func.lower(Author.AuthorName).contains(func.lower(kw)),
                               func.lower(Publisher.Publisher_Name).contains(func.lower(kw))),
                               func.lower(Author.FullName).contains(func.lower(kw)),
                               func.lower(Publisher.Publisher_Name).contains(func.lower(kw)))

    if cate_id:
        book = Book.filter(Book.Category_ID.__eq__(cate_id))

    if page:
        page = int(page)
        page_size = app.config["PAGE_SIZE"]
        start = (page - 1) * page_size

        return book.slice(start, start + page_size)

    return book.all()


def get_user_by_id(account_id):
    return Account.query.get(account_id)

def get_quantity_in_stock(book_id):
    book = Book.query.filter_by(Book_ID=book_id).first()
    return book.QuantityInStock if book else None


def add_bill(cart, delivery_method, customer_id):
    try:
        customer_id = session.get('customer_id')
        delivery_method = session.get('delivery_method')

        if customer_id and delivery_method:
            # Kiểm tra giá trị của Book_Receive_At để thiết lập giá trị state
            state = False if delivery_method == 'pickupAtStore' else None
            bill = Bill(Customer_ID=customer_id, Book_Receive_At=delivery_method, IsCancel=state)
            db.session.add(bill)

            for c in cart.values():
                book = Book.query.get(c["Book_ID"])

                if book and book.QuantityInStock >= c["quantity"]:
                    book.QuantityInStock -= c["quantity"]
                    db.session.commit()
                    d = BillDetail(Quantity=c["quantity"],
                                   Total_Amount=c["Price"],
                                   Book_ID=c["Book_ID"],
                                   bill=bill)
                    db.session.add(d)
            db.session.commit()
            print("Giao dịch đã được thêm thành công.")
            return True
        else:
            print("Không tìm thấy khách hàng.")
            return False
    except Exception as e:
        print(f"Lỗi trong quá trình thêm hóa đơn: {str(e)}")
        return False

