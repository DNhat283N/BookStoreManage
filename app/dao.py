from app.models import Category, Book, Account, Author, Publisher
from app import app
import hashlib
from sqlalchemy import func, or_


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
                               func.lower(Publisher.Publish_Name).contains(func.lower(kw))))

    if cate_id:
        book = book.filter(Book.Category_ID.__eq__(cate_id))

    if page:
        page = int(page)
        page_size = app.config["PAGE_SIZE"]
        start = (page - 1) * page_size

        return book.slice(start, start + page_size)

    return book.all()


def get_user_by_id(account_id):
    return Account.query.get(account_id)
