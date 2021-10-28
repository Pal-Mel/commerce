from django.urls import path
from . import views

app_name="user"

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.login_view, name="login"),
    # path('login/<path>', views.login_view_redirect, name="login_redirect"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]

