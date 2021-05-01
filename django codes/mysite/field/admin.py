from django.contrib import admin

from .models import Moisture, Humidity, Temperature, Light

admin.site.register(Moisture)
admin.site.register(Humidity)
admin.site.register(Temperature)
admin.site.register(Light)
