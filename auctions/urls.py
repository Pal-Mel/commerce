from django.urls import path

from . import views

app_name='auction'

urlpatterns = [
    path("", views.index, name="index"),
    path('<id>',views.getAuction,name="getAuction"),
]
