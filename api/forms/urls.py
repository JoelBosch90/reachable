from django.urls import path
from . import views

# This is where we list our API endpoints.
urlpatterns = [
  path("forms/", views.FormList.as_view()),
  path("forms/<int:pk>", views.FormDetail.as_view()),
  path("links/", views.LinkList.as_view()),
  path("links/<int:pk>", views.LinkDetail.as_view()),
  path("inputs/", views.InputList.as_view()),
  path("inputs/<int:pk>", views.InputDetail.as_view()),
]