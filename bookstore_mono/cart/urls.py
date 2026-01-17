from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_item, name='remove_item'),  # Thêm dòng này
    path('', views.view_cart, name='cart_detail'),
]