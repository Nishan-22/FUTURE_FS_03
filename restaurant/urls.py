from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('add_to_order/<int:item_id>/', views.add_to_order, name='add_to_order'),
    path('order/', views.order_view, name='order_view'),
    path('update_order_quantity/<int:item_id>/', views.update_order_quantity, name='update_order_quantity'),
    path('remove_from_order/<int:item_id>/', views.remove_from_order, name='remove_from_order'),
    path('checkout/', views.checkout, name='checkout'),
    path('reserve/', views.reservation_view, name='reservation_view'),
    path('contact/', views.contact_us, name='contact_us'),
    path('review/', views.submit_review, name='submit_review'),
    path('staff/login/', views.staff_login, name='staff_login'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/order/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
    path('staff/reservation/<int:reservation_id>/confirm/', views.confirm_reservation_staff, name='confirm_reservation_staff'),
    path('staff/menu/add/', views.add_menu_item, name='add_menu_item'),
    path('staff/menu/<int:item_id>/edit/', views.edit_menu_item, name='edit_menu_item'),
    path('staff/menu/<int:item_id>/delete/', views.delete_menu_item, name='delete_menu_item'),
]