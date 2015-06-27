from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.html import urlize as urlize_impl

from woot.apps.catalog.models.interactions import Interaction, UserInteraction

import re

register = template.Library()

@register.filter(is_safe=True, needs_autoescape=True)
@stringfilter
def urlize_target_blank(value, limit, autoescape=None):
    '''
    This tag extends the default 'urlize' filter in Django.
    Apart from urlizing the text, it opens the links in a new window
    '''
    if limit is not None:
        limit = int(limit)
    return mark_safe(urlize_impl(value, trim_url_limit=limit,
                     nofollow=True, autoescape=autoescape).
                     replace('<a', '<a target="_blank"'))

@register.filter
def activity_type(obj):
    interaction = Interaction.from_id(obj.event)
    return interaction.name

@register.filter
def highlight(text, word):
    return mark_safe(re.compile(r'('+word+')', re.IGNORECASE).sub(r'<span class="highlight">\1</span>', text));
