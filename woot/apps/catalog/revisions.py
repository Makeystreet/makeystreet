import reversion

from apps.catalog.models.core import *
from django.contrib.auth.models import User

reversion.register(Note)
reversion.register(User)
reversion.register(Comment)
reversion.register(Documentation)
reversion.register(Image)
reversion.register(Video)
reversion.register(Product)

reversion.register(Makey, follow=['collaborators', 'comments', 'notes',
                                  'documentations', 'images', 'cover_pic',
                                  'videos', ])
