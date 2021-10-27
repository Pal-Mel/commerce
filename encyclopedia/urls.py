from django.urls import path

from . import views

app_name ="enc"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>",views.article, name="article"),
    path("search/",views.search, name="search"),
    path("add/",views.add, name="add"),
    path("edit/<str:name>",views.edit, name="edit"),
    path("edit",views.saveedit, name="saveedit"),
    path("randompage",views.randompage, name="randompage"),
]
