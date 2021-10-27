from django.contrib import admin
from .models import *

# Реєструємо ваші моделі.
admin.site.register(User)
admin.site.register(Profile)

