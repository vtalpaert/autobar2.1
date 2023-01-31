from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ArtistsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "robotcocktail.artists"
    verbose_name = _("Artists")

    def ready(self):
        try:
            import robotcocktail.artists.signals  # noqa F401
        except ImportError:
            pass
