from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='user_index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.user_password, name='user_password'),
    path('reservations/', views.user_reservations, name='user_reservations'),
    path('reservationsdetail/<int:id>/', views.user_reservationsdetail, name='user_reservationsdetail'),
    path('comments/', views.user_comments, name='user_comments'),
    path('deletecomment/<int:id>', views.user_deletecomment, name='user_deletecomment'),

]
