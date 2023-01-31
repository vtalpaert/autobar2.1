from django.contrib import admin, messages
from django.utils.translation import ngettext

from robotcocktail.artists.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # inlines = (SubscriptionsInline, )
    list_display = (
        "user",
        "artist_name",
        "location",
        "bio",
    )
    actions = ("reset_profile",)

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.action(description="Reset selected profiles")
    def reset_profile(self, request, queryset):
        resets = 0
        for profile in queryset:
            profile.set_default_values()
            resets += 1
        self.message_user(
            request,
            ngettext(
                "%d profile was successfully reset to default.",
                "%d profiles were successfully reset to defaults.",
                resets,
            )
            % resets,
            messages.SUCCESS,
        )
