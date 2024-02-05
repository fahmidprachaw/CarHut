from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CarListView.as_view() ,name='carList'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.Profile, name='profile'),
    path('car/<int:pk>/', views.CarDelailView.as_view(), name='car_detail'),
    path('buy_car/<int:pk>/', views.BuyCarView.as_view(), name='buy_car'),
    path('order/', views.OrderHistoryView.as_view(), name='order_car'),
    path('passchange/', views.change_password, name='passchange'),
]
