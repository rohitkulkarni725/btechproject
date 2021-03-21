from django.urls import path

from . import views

app_name = 'ota'
urlpatterns = [
    path('', views.index, name='index'),
    path('editmod', views.editmod, name='editmod'),
    path('details', views.details, name='details'),
    path('error', views.error, name='error')
]