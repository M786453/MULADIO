from django.urls import path
from . import views

urlpatterns = [
    path('', views.muladio,name='muladio')
]