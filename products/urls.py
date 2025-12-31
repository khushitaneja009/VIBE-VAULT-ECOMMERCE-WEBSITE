from django.urls import path
from .views import *
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('all_products'), name='home'),
    path('categories/', category_list, name='category_list'),
    path('products/<int:category_id>/', product_list, name='product_list'),
    path('products/', product_list, name='all_products'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('cart/', cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/count/', cart_count, name='cart_count'),
    path('cart/update/<int:item_id>/', update_quantity, name='update_quantity'),
    path('cart/remove/<int:item_id>/', remove_item, name='remove_item'),
    path('order/', Order_view, name='order'),
    path('order/submit/', submit_order, name='submit_order'),
    path('Thanks/', thank_you, name='Thanks_view'),
]
