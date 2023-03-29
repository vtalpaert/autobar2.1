from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

User = get_user_model()


def _cut(value, low=None, high=None):
    if low:
        value = max(low, value)
    if high:
        value = min(high, value)
    return value


class Profile(models.Model):
    # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    artist_name = models.CharField(
        blank=True,
        max_length=30,
        help_text=_("An artistry name. This is your public name."),
    )
    # TODO: add a bar name
    bio = models.TextField(
        max_length=500, blank=True, help_text=_("An impressive biography.")
    )
    location = models.CharField(
        max_length=50, blank=True, help_text=_("Tell the world where you are from.")
    )
    follow_requests = models.ManyToManyField(
        "self", through="FollowRequest", through_fields=("from_profile", "to_profile")
    )

    def __str__(self):
        return self.user.username

    @property
    def my_followers(self):
        return self.follow_requests_received.filter(status=FollowRequest.ACCEPTED)

    @property
    def my_following(self):
        return self.follow_requests_sent.filter(status=FollowRequest.ACCEPTED)

    def my_request_to(self, profile):
        try:
            return self.follow_requests_sent.get(to_profile=profile)
        except FollowRequest.DoesNotExist:
            return

    def set_default_values(self):
        self.artist_name = self.user.username
        self.location = ""
        self.bio = _("This is my bio\nIt is publicly visible to all logged in users.")
        self.follow_requests.clear()
        self.save()


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        profile = Profile(user=user)
        profile.save()
        profile.set_default_values()


post_save.connect(create_profile, sender=User)


class FollowRequest(models.Model):
    "Request for a single direction access to the mixes portfolio of an artist"

    class Meta:
        unique_together = [["from_profile", "to_profile"]]

    CREATED = 0
    ACCEPTED = 1
    REJECTED = 2
    STATUS = [
        (CREATED, "Created"),
        (ACCEPTED, "Accepted"),
        (REJECTED, "Rejected"),
    ]
    status = models.SmallIntegerField(choices=STATUS, default=CREATED)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    from_profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="follow_requests_sent"
    )
    to_profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="follow_requests_received"
    )
    message = models.TextField(max_length=200, blank=True, help_text=_("Message"))

    def accept(self):
        if self.status is not self.ACCEPTED:
            self.status = self.ACCEPTED
            self.save()

    def reject(self):
        if self.status is not self.REJECTED:
            self.status = self.REJECTED
            self.save()

    def __str__(self):
        return f"FR {self.from_profile} to {self.to_profile}: {self.STATUS[self.status][1]}"


class Ingredient(models.Model):
    class Meta:
        ordering = ("name",)

    # Handling of units for mass and volume
    UNIT_DENSITY = "g/L"
    UNIT_DENSITY_DEFAULT = 1000  # default density for liquids in [UNIT_DENSITY]
    UNIT_VOLUME = "cL"
    UNIT_VOLUME_VERBOSE = "centiliter"
    UNIT_MASS = "g"
    UNIT_MASS_VERBOSE = "gram"
    FACTOR_VOLUME_TO_MASS = 10  # 1 cL is 10 g
    SHOT_VOLUME = 5  # [cL]

    # States
    SOLID = 0
    SYRUP = 1
    CARBONATED = 2
    STILL = 3
    LIQUIDS = (SYRUP, CARBONATED, STILL)
    STATE_CHOICES = [
        (SOLID, "Solid"),
        (SYRUP, "Syrup"),
        (CARBONATED, "Carbonated"),
        (STILL, "Still"),
    ]
    state = models.SmallIntegerField(choices=STATE_CHOICES)

    name = models.CharField(unique=True, max_length=50)
    is_alcohol = models.BooleanField(
        help_text="Does this ingredient contain any alcohol?"
    )
    alcohol_percentage = models.FloatField(help_text="Should be between 0 and 100")
    density = models.FloatField(
        help_text="In grams per liter [%s]" % UNIT_DENSITY, default=UNIT_DENSITY_DEFAULT
    )

    def save(self, *args, **kwargs):
        if self.is_alcohol:
            self.alcohol_percentage = _cut(self.alcohol_percentage, low=1, high=100)
        else:
            self.alcohol_percentage = 0
        self.density = _cut(self.density, low=0)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
