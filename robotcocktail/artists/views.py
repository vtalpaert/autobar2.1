from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, UpdateView

from .models import Profile

User = get_user_model()


class ProfileDetailView(LoginRequiredMixin, DetailView):

    model = Profile

    def get_object(self):
        return self.request.user.profile


profile_detail_view = ProfileDetailView.as_view()


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = Profile
    fields = [
        "artist_name",
        "location",
        "bio",
    ]
    success_message = _("Information successfully updated")

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return reverse("artists:detail")


profile_update_view = ProfileUpdateView.as_view()
