import enum
import hashlib
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, CHAR, Date, DateTime
from sqlalchemy.orm import relationship

from app import db, app


class Category(db.Model):
    __tablename__ = 'Category'
    Category_ID = Column(Integer, primary_key=True, autoincrement=True)
    Category_Name = Column(String(255), nullable=False, unique=True)

    books = relationship('Book', backref='category', lazy=True)


class UserRoleEnum(enum.Enum):
    ADMIN = 1
    STAFF = 2


class PersonModel(db.Model):
    __abstract__ = True
    FullName = Column(String(255), nullable=True)
    Gender = Column(String(10), nullable=True)
    BirthDay = Column(Date, nullable=False)

    def __str__(self):
        return self.FullName


class Customer(PersonModel):
    __tablename__ = 'Customer'

    Customer_ID = Column(CHAR(12), primary_key=True, nullable=True)
    phone_number = relationship('PhoneNumber', backref='customer', lazy=True)
    bill = relationship('Bill', backref='customer', lazy=True)
    delivery_of_customer = relationship('DeliveryOfCustomer', backref='customer', lazy=True)


class Staff(PersonModel):
    Staff_ID = Column(Integer, primary_key=True, nullable=True)
    Starting_Date = Column(DateTime, default=datetime.now())
    Position = Column(Enum(UserRoleEnum), default=UserRoleEnum.STAFF)

    account = relationship('Account', backref='staff', lazy=True)


class Author(PersonModel):
    __tablename__ = 'Author'
    Author_ID = Column(Integer, primary_key=True, nullable=True)
    books = relationship('Book', backref='author', lazy=True)


class Publisher(db.Model):
    __tablename__ = 'Publisher'
    Publisher_ID = Column(Integer, primary_key=True, autoincrement=True)
    Publisher_Name = Column(String(255), nullable=False, unique=True)
    Publisher_Address = Column(String(255), nullable=False, unique=True)

    books = relationship('Book', backref='publisher', lazy=True)

    def __str__(self):
        return self.Publisher_Name


class Book(db.Model):
    __tablename__ = 'Book'
    Book_ID = Column(Integer, primary_key=True, autoincrement=True)
    BookName = Column(String(50), nullable=False, unique=True)
    Price = Column(Float, default=0)
    Image = Column(String(255), default=True)
    BookInfo = Column(String(1000), default=True, nullable=False)
    QuantityInStock = Column(Integer, nullable=False, default=0)

    Category_ID = Column(Integer, ForeignKey(Category.Category_ID), nullable=False)
    Author_ID = Column(Integer, ForeignKey(Author.Author_ID), nullable=False)

    Publisher_ID = Column(Integer, ForeignKey(Publisher.Publisher_ID), nullable=False)

    bill_detail = relationship('BillDetail', backref='book', lazy=True)

    def __str__(self):
        return self.BookName


class Account(db.Model, UserMixin):
    __tablename__ = 'Account'

    Account_ID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50), nullable=False, unique=True)
    Username = Column(String(50), nullable=False, unique=True)
    Password = Column(String(50), nullable=False)
    User_Role = Column(Enum(UserRoleEnum), default=UserRoleEnum.STAFF)

    Staff_ID = Column(Integer, ForeignKey(Staff.Staff_ID), nullable=False)

    def __str__(self):
        return self.Name

    def get_id(self):
        return str(self.Account_ID)


class PhoneNumber(db.Model):
    __tablename__ = 'PhoneNumber'
    Phone_Number_ID = Column(Integer, primary_key=True, autoincrement=True)
    Phone_Number = Column(CHAR(10), nullable=True, unique=True)

    Customer_ID = Column(CHAR(10), ForeignKey(Customer.Customer_ID), nullable=False)


class DeliveryAddress(db.Model):
    __tablename__ = 'DeliveryAddress'
    Address_ID = Column(Integer, primary_key=True, autoincrement=True)
    Address = Column(String(255), nullable=True)

    delivery_of_customer = relationship('DeliveryOfCustomer', backref='address', lazy=True)


class DeliveryOfCustomer(db.Model):
    DOC_ID = Column(Integer, primary_key=True, autoincrement=True)

    Address_ID = Column(Integer, ForeignKey(DeliveryAddress.Address_ID), nullable=False)
    Customer_ID = Column(CHAR(10), ForeignKey(Customer.Customer_ID), nullable=False)


class Bill(db.Model):
    __tablename__ = 'Bill'
    Bill_ID = Column(Integer, primary_key=True, autoincrement=True)
    Total_Amount = Column(Integer, nullable=True)
    Book_Receive_At = Column(Boolean, nullable=False)
    State = Column(Integer, nullable=False)
    Customer_ID = Column(CHAR(10), ForeignKey(Customer.Customer_ID), nullable=False)

    bill_detail = relationship('BillDetail', backref='bill', lazy=True)


class BillDetail(db.Model):
    __tablename_ = 'BillDetail'
    Bill_Detail_ID = Column(Integer, primary_key=True, autoincrement=True)
    Quantity = Column(Integer, nullable=False, default=0)
    Order_Date = Column(DateTime, default=datetime.now())

    Bill_ID = Column(Integer, ForeignKey(Bill.Bill_ID), nullable=False)
    Book_ID = Column(Integer, ForeignKey(Book.Book_ID), nullable=False)


class BookConfig(db.Model):
    Config_ID = Column(Integer, primary_key=True, autoincrement=True)
    Config_Name = Column(String(50), nullable=False, unique=True)
    Config_Quantity = Column(Integer, nullable=False)
    Config_Unit = Column(String(50), nullable=False)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        c1 = Category(Category_Name="Tiểu thuyết")
        c2 = Category(Category_Name="Trinh thám ")
        c3 = Category(Category_Name="Kinh doanh và tài chính")
        c4 = Category(Category_Name="Tâm lý học")
        c5 = Category(Category_Name="Khoa học và Thiên văn học ")
        c6 = Category(Category_Name="Lịch sử và Văn hóa")
        c7 = Category(Category_Name="Nấu ăn và ẩm thực ")
        c8 = Category(Category_Name="Trẻ em và thiếu nhi")
        db.session.add_all([c1, c2, c3, c4, c5, c6, c7, c8])
        db.session.commit()

        p1 = Publisher(Publisher_Name="Nhà xuất bản Trẻ",
                       Publisher_Address="161B Lý Chính Thắng; Phường 7; Quận 3; Thành phố Hồ Chí Minh.")
        p2 = Publisher(Publisher_Name="Nhà xuất bản Kim Đồng",
                       Publisher_Address="248 Đ. Cống Quỳnh, Phường Phạm Ngũ Lão, Quận 1, Thành phố Hồ Chí Minh")
        p3 = Publisher(Publisher_Name="Nhà xuất bản Tổng hợp thành phố Hồ Chí Minh",
                       Publisher_Address="62 Nguyễn Thị Minh Khai, phường Đa Kao, quận 1, TPHCM")
        p4 = Publisher(Publisher_Name="Nhà xuất bản Lao Động", Publisher_Address="82 Trần Hưng Đạo, Hà Nộ")
        p5 = Publisher(Publisher_Name="Nhà xuất bản Hội Nhà văn",
                       Publisher_Address="65, Nguyễn Du, quận Hai Bà Trưng, Hà Nội")
        db.session.add_all([p1, p2, p3, p4, p5])
        db.session.commit()

        a1 = Author(FullName='Nguyễn Ái Quốc', Gender='Nam', BirthDay='1980-05-19')
        a2 = Author(FullName='Hồ Xuân Hương', Gender='Nữ', BirthDay='1772/07/10')
        a3 = Author(FullName='Nguyễn Du', Gender='Nam', BirthDay='1776/01/03')
        a4 = Author(FullName='Nguyễn Nhật Ánh', Gender='Nam', BirthDay='1955/05/07')
        a5 = Author(FullName='Nguyễn Ngọc Thạch', Gender='Nam', BirthDay='1987/01/02')
        db.session.add_all([a1, a2, a3, a4, a5])
        db.session.commit()

        s1 = Book(BookName="Mười người da đen nhỏ", Price=135000, Category_ID=1, Author_ID='1', Publisher_ID=1,
                  Image="https://i.pinimg.com/originals/91/76/9a/91769a5f3c3d663cc3c2152e9fadabf0.jpg",
                  QuantityInStock=5,
                  BookInfo="Tiểu thuyết nói về vụ án bí ẩn trên hòn đảo Soldier Island với 10 người bằng cách này hay cách khác đã thiệt mạng mà không hề có sự hiện diện hay dấu vết của thủ phạm")
        s2 = Book(BookName="Phía Sau Nghi Can X ", Price=150000, Category_ID=2, Author_ID='2', Publisher_ID=2,
                  Image="https://i.pinimg.com/originals/91/76/9a/91769a5f3c3d663cc3c2152e9fadabf0.jpg",
                  QuantityInStock=5,
                  BookInfo="Tiểu thuyết nói về vụ án bí ẩn trên hòn đảo Soldier Island với 10 người bằng cách này hay cách khác đã thiệt mạng mà không hề có sự hiện diện hay dấu vết của thủ phạm")
        s3 = Book(BookName="Bí quyết gây dựng cơ nghiệp bạc tỷ", Price=135000, Category_ID=3, Author_ID='3',
                  Publisher_ID=3,
                  Image="https://i.pinimg.com/originals/91/76/9a/91769a5f3c3d663cc3c2152e9fadabf0.jpg",
                  QuantityInStock=5,
                  BookInfo="Tiểu thuyết nói về vụ án bí ẩn trên hòn đảo Soldier Island với 10 người bằng cách này hay cách khác đã thiệt mạng mà không hề có sự hiện diện hay dấu vết của thủ phạm")
        s4 = Book(BookName="Tâm lý học đám đông", Price=135000, Category_ID=4, Author_ID='4', Publisher_ID=4,
                  Image="https://i.pinimg.com/originals/91/76/9a/91769a5f3c3d663cc3c2152e9fadabf0.jpg",
                  QuantityInStock=5,
                  BookInfo="Tiểu thuyết nói về vụ án bí ẩn trên hòn đảo Soldier Island với 10 người bằng cách này hay cách khác đã thiệt mạng mà không hề có sự hiện diện hay dấu vết của thủ phạm")
        s5 = Book(BookName="Từ điển thiên văn học và vật lý thiên văn", Price=135000, Category_ID=5, Author_ID='5',
                  Publisher_ID=5,
                  Image="https://i.pinimg.com/originals/91/76/9a/91769a5f3c3d663cc3c2152e9fadabf0.jpg",
                  QuantityInStock=5,
                  BookInfo="Tiểu thuyết nói về vụ án bí ẩn trên hòn đảo Soldier Island với 10 người bằng cách này hay cách khác đã thiệt mạng mà không hề có sự hiện diện hay dấu vết của thủ phạm")
        s6 = Book(BookName="Lịch sử và văn hóa Đông Nam Á", Price=135000, Category_ID=6, Author_ID='1', Publisher_ID=1,
                  Image="https://i.pinimg.com/originals/91/76/9a/91769a5f3c3d663cc3c2152e9fadabf0.jpg",
                  QuantityInStock=5,
                  BookInfo="Tiểu thuyết nói về vụ án bí ẩn trên hòn đảo Soldier Island với 10 người bằng cách này hay cách khác đã thiệt mạng mà không hề có sự hiện diện hay dấu vết của thủ phạm")
        s7 = Book(BookName="Ăn uống thời hiện đại", Price=135000, Category_ID=7, Author_ID='2', Publisher_ID=2,
                  Image="https://i.pinimg.com/originals/91/76/9a/91769a5f3c3d663cc3c2152e9fadabf0.jpg",
                  QuantityInStock=5,
                  BookInfo="Tiểu thuyết nói về vụ án bí ẩn trên hòn đảo Soldier Island với 10 người bằng cách này hay cách khác đã thiệt mạng mà không hề có sự hiện diện hay dấu vết của thủ phạm")
        s8 = Book(BookName="Kể truyện cho bé tuổi mầm non", Price=135000, Category_ID=8, Author_ID='3', Publisher_ID=3,
                  Image="https://i.pinimg.com/originals/91/76/9a/91769a5f3c3d663cc3c2152e9fadabf0.jpg",
                  QuantityInStock=5,
                  BookInfo="Tiểu thuyết nói về vụ án bí ẩn trên hòn đảo Soldier Island với 10 người bằng cách này hay cách khác đã thiệt mạng mà không hề có sự hiện diện hay dấu vết của thủ phạm")
        s9 = Book(BookName="Tiểu thuyết hay 2021", Price=135000, Category_ID=1, Author_ID='4', Publisher_ID=4,
                  Image="https://i.pinimg.com/originals/91/76/9a/91769a5f3c3d663cc3c2152e9fadabf0.jpg",
                  QuantityInStock=5,
                  BookInfo="Tiểu thuyết nói về vụ án bí ẩn trên hòn đảo Soldier Island với 10 người bằng cách này hay cách khác đã thiệt mạng mà không hề có sự hiện diện hay dấu vết của thủ phạm")
        s10 = Book(BookName="Mật mã Da Vinci", Price=135000, Category_ID=2, Author_ID='5', Publisher_ID=5,
                   Image="https://i.pinimg.com/originals/91/76/9a/91769a5f3c3d663cc3c2152e9fadabf0.jpg",
                   QuantityInStock=5,
                   BookInfo="Tiểu thuyết nói về vụ án bí ẩn trên hòn đảo Soldier Island với 10 người bằng cách này hay cách khác đã thiệt mạng mà không hề có sự hiện diện hay dấu vết của thủ phạm")
        db.session.add_all([s1, s2, s3, s4, s5, s6, s7, s8, s9, s10])
        db.session.commit()

        t1 = Staff(FullName="Nguyễn Đình Nhật", BirthDay='2003-08-29', Gender="Nam", Position=UserRoleEnum.ADMIN,
                   Starting_Date='2023-12-01')
        db.session.add(t1)
        db.session.commit()

        u1 = Account(Name='Admin', Username="admin",
                     Password=str(hashlib.md5('12345'.encode('utf-8')).hexdigest()),
                     User_Role=UserRoleEnum.ADMIN, Staff_ID = 1)
        db.session.add_all([u1])
        db.session.commit()

        cf1 = BookConfig(Config_ID=1, Config_Name="Minimum Quantity In Stock",
                         Config_Quantity="150", Config_Unit="Quyển")
        cf2 = BookConfig(Config_ID=2, Config_Name="Minimum Input Quantity",
                         Config_Quantity="50", Config_Unit="Quyển")
        cf3 = BookConfig(Config_ID=3, Config_Name="Cancel Order Time", Config_Quantity="48", Config_Unit="Giờ")
        db.session.add_all([cf1, cf2, cf3])
        db.session.commit()
