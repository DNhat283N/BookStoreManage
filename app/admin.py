from flask import redirect, request, render_template
from flask_admin import Admin, BaseView, expose, menu, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user

from app import app, db, dao
from app.models import Category, Book, UserRoleEnum, BookConfig


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
    column_list = ['Book_ID', 'BookName', 'Price', 'QuantityInStock', 'Category_ID']
    column_filters = ['BookName', 'Category_ID', 'Publisher_ID', 'Author_ID']


class TableStatsView(AuthenticatedUserView):
    @expose('/')
    def index(self):
        kwd = request.args.get('kwd')
        if kwd:
            return self.render('admin/stats_with_table.html', stats=dao.stats_revenue(kwd), kw=kwd)
        return self.render('admin/stats_with_table.html', stats=dao.stats_revenue(kwd), kw="")


class ChartStatsView(AuthenticatedUserView):
    @expose('/')
    def index(self):
        kwd = request.args.get('kwd')
        if kwd:
            return self.render('admin/stats_with_chart.html', stats=dao.stats_revenue(kwd), kw=kwd)
        return self.render('admin/stats_with_chart.html', stats=dao.stats_revenue(kwd), kw="")


class LogOutView(AuthenticatedUserView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class ConfigView(AuthenticatedAdminView):
    column_list = ['Config_ID', 'Config_Name', 'Config_Quantity', 'Config_Unit']


stats_category = menu.MenuCategory('Statistic', class_name='dropdown')

admin = Admin(app=app, name='Quản Trị Bán Hàng Nhà Sách', template_mode='bootstrap4')
admin.add_view(CategoryView(Category, db.session))
admin.add_view(BookView(Book, db.session))
admin.add_view(ConfigView(BookConfig, db.session))

admin.add_menu_item(stats_category)
admin.add_view(TableStatsView(name="Table Format", category='Statistic'))
admin.add_view(ChartStatsView(name="Chart Format", category='Statistic'))

admin.add_view(LogOutView(name="Log Out"))

if __name__ == '__main__':
    with app.app_context():
        print(dao.stats_revenue())
