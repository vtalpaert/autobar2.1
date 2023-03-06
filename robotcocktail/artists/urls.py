from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from robotcocktail.artists import views

app_name = "artists"
urlpatterns = [
    path("myprofile/~edit/", view=views.profile_update_view, name="update"),
    path("myprofile/", view=views.profile_detail_view, name="detail"),
    path("profile/<str:username>/", view=views.profile_detail_view, name="detail"),
] + format_suffix_patterns(
    [
        path("mysentfollowrequest/", views.MySentFollowRequestList.as_view()),
        path("myreceivedfollowrequest/", views.MyReceivedFollowRequestList.as_view()),
        path("followrequest/<int:pk>/", views.FollowRequestDetail.as_view()),
    ]
)
