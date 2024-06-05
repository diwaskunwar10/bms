from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name=""),
    path('register',views.register,name="register"),
    path('login',views.login,name="login"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('user-logout', views.user_logout, name="user-logout"),
    # path('checkout', views.checkout, name="checkout"),
    path('checkout/', views.checkout, name='checkout'),

    # path('fetch/', views.fetch_data, name='fetch_data'),



]