from django.urls import path

from . import views

app_name='auction'

urlpatterns = [
    path("", views.index, name="index"), # всі аукціони
    path("", views.index, name="changeCategoryAuction"), # всі аукціони
    path("active", views.indexActive, name="indexActive"), # активні аукціони
    path("active", views.indexActive, name="changeCategoryActiveAuction"), # Активні аукціони
    path("watch", views.indexWatchList, name="indexWatchList"), # активні аукціони
   
    path('<id>',views.getAuction,name="getAuction"),
]
