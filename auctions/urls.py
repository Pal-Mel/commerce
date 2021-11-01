from django.urls import path

from . import views

app_name='auction'

urlpatterns = [
    path("", views.index, name="index"), # всі аукціони
    path("", views.index, name="changeCategoryAuction"), # всі аукціони
    path("addWatch/<id>", views.addWatch, name="addWatch"), #  Додавання до списку спостереження
    path("makeRate/<id>/<minRate>", views.makeRate, name="makeRate"), # зробити ставку

    path("addAuction", views.addAuction, name="addAuction"), # додати аукціони
    path("closeAuction/<id>", views.closeAuction, name="closeAuction"), #  Закрити аукціон
    path("active", views.indexActive, name="indexActive"), # активні аукціони
    path("active", views.indexActive, name="changeCategoryActiveAuction"), # Активні аукціони
    path("watch", views.indexWatchList, name="indexWatchList"), # активні аукціони
    path('<id>',views.getAuction,name="getAuction"),
]
