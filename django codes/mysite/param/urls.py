from django.urls import path

from . import views

app_name = 'param'
urlpatterns = [
    path('', views.index, name='index')
]
