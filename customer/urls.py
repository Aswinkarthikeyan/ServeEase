from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.customer_home,
        name='customer_home'
    ),

    path(
        'login/',
        views.customer_login,
        name='login'
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'order/create/',
        views.create_order,
        name='create_order'
    ),

    path(
        'order/booked-slots/',
        views.get_booked_slots,
        name='get_booked_slots'
    ),

    path(
        'profile/edit/',
        views.customer_edit_profile,
        name='customer_edit_profile'
    ),

    path(
        'logout/',
        views.customer_logout,
        name='customer_logout'
    ),
]