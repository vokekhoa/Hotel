from hotelapp import admin, db
from hotelapp.models import Category, Room
from flask_admin.contrib.sqla import ModelView

class ProductView(ModelView):
    column_display_pk = True
    can_view_details = True
    column_filters = ['name', 'price', 'category']
    column_searchable_list = ['name']
    can_export = True
    column_exclude_list = ['image', 'active']
    column_labels = {
        'name': 'Tên phòng',
        'description': 'Mô tả',
        'price': 'Giá',
        'image': 'Ảnh đại diện',
        'category': 'Danh mục'
    }
    column_sortable_list = ['id', 'name', 'price']

admin.add_view(ModelView(Category, db.session))
admin.add_view(ProductView(Room, db.session))