from django.urls import path

from . import views

app_name = "wagtail_active_campaign"

urlpatterns = [
    path("", views.index, name="index"),
]
