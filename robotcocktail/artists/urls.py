from django.urls import path

from robotcocktail.artists.views import profile_detail_view, profile_update_view

app_name = "artists"
urlpatterns = [
    path("myprofile/~edit/", view=profile_update_view, name="update"),
    path("myprofile/", view=profile_detail_view, name="detail"),
]
