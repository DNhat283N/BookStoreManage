from app.models import Category, Book, UserRoleEnum
from app import app, db, dao
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask import redirect, request, Flask, session


class AuthenticatedAdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.User_Role == UserRoleEnum.ADMIN


class AuthenticatedUserView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class CategoryView(AuthenticatedAdminView):
    column_list = ['Category_ID', 'Category_Name']
    column_filters = ['Category_Name']


class BookView(AuthenticatedAdminView):
    column_list = ['Book_ID', 'BookName', 'Price', 'QuantityInStock', 'Category_Name']
    column_filters = ['BookName', 'Category_ID', 'Publisher_ID', 'Author_ID']


class StatsView(AuthenticatedUserView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


class LogOutView(AuthenticatedUserView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


admin = Admin(app=app, name='Quản Trị Bán Hàng Nhà Sách', template_mode='bootstrap4')
admin.add_view(CategoryView(Category, db.session))
admin.add_view(BookView(Book, db.session))
admin.add_view(StatsView(name="Statistic"))
admin.add_view(LogOutView(name="Log Out"))
