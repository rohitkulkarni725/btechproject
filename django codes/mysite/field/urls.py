from django.urls import path

from . import views

app_name = 'field'
urlpatterns = [
    path('', views.index, name='index'),
    path('editfld', views.editfld, name='editfld'),
    path('details', views.details, name='details'),
    path('error', views.error, name='error')
]