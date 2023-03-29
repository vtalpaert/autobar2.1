from django import template

from robotcocktail.artists.models import Ingredient

register = template.Library()


_state_choices = {val: name for val, name in Ingredient.STATE_CHOICES}


@register.filter(is_safe=True)
def ingredient_state(value):
    return _state_choices[value]
