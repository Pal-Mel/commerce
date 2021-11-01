from django.contrib import admin

# Register your models here.
from .models import *

# Реєструємо ваші моделі.
admin.site.register(Categori)
admin.site.register(Status)
admin.site.register(Auction)
admin.site.register(Rates)
admin.site.register(Comments)
admin.site.register(WatchAuction)


