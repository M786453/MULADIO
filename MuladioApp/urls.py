from django.urls import path,re_path
from . import views

urlpatterns = [
    path("", views.muladio, name="muladio"),
    path("generate", views.generate, name="generate"),
    path("clean", views.clean, name="clean")

]