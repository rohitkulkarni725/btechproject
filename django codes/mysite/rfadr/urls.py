from django.urls import path

from . import views

app_name = 'rfadr'
urlpatterns = [
    path('', views.index, name='index'),
    path('editadr', views.editadr, name='editadr'),
    path('details', views.details, name='details'),
    path('error', views.error, name='error')
]