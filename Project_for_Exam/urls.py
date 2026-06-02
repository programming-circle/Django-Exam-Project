from django.urls import path, include
from . import views

urlpatterns = [
    path('sing_up/', views.register_page, name="register_page"),
    path('newuser/', views.register_view, name="new_user"),
    path('auth/', views.auth_page, name="auth_page"),
    path('login/',views.login_page, name="login_page"),
    path('login-view', views.login_view, name="login_view"),
    path('logout/', views.logout_view,name="logout"),

    path('main/', views.main, name="main_page"),

    #staff urls

    path('staff/dashboard/',views.staff_dashboard,name="dashboard")

]