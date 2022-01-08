from django.urls import path
from . import views

# This is where we list our API endpoints.
urlpatterns = [
    path("forms/", views.FormListView.as_view()),
    path("forms/response/", views.FormResponseView.as_view()),
    path("forms/<int:pk>", views.FormDetailView.as_view()),
    path("forms/link/<key>", views.FormLinkView.as_view()),
    path("forms/confirm/<key>", views.FormConfirmationView.as_view()),
    path("forms/disable/<key>", views.FormDisableView.as_view()),
    path("links/", views.FormLinkListView.as_view()),
    path("links/<key>", views.FormLinkDetailView.as_view()),
    path("inputs/", views.InputListView.as_view()),
    path("inputs/<int:pk>", views.InputDetailView.as_view()),
]
