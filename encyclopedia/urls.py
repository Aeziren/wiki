from django.urls import path

from . import views

app_name = 'wiki'

urlpatterns = [
    path("random", views.random_page, name="random"),
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("wiki/<str:title>", views.content, name="content"),
    path("new", views.new, name="new"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
]
