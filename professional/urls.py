from django.urls import path

from . import views


urlpatterns = [

    path(
        'pending/',
        views.professional_pending,
        name='professional_pending'
    ),

    path(
        'home/',
        views.professional_home,
        name='professional_home'
    ),

    path(
        'order/<int:order_id>/<str:action>/',
        views.update_order,
        name='update_order'
    ),

    path(
        'edit-profile/',
        views.professional_edit_profile,
        name='professional_edit_profile'
    ),

    path(
        'logout/',
        views.professional_logout,
        name='professional_logout'
    ),
]