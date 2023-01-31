from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Profile(models.Model):
    # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    artist_name = models.CharField(blank=True, max_length=255)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username

    def set_default_values(self):
        self.artist_name = self.user.username
        self.location = _("Unknown")
        self.bio = _("This is my bio")
        self.save()


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        profile = Profile(user=user)
        profile.set_default_values()


post_save.connect(create_profile, sender=User)
