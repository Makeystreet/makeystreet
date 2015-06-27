from datetime import datetime
import operator
import string
import unicodedata

from django.conf import settings
from django.core.context_processors import csrf
from django.db.models import Q
from django.template import RequestContext, Template, Context

from forms import TutorialForm, MakeyForm
from models.core import ProductShopUrl, Product, ProductDescription, User, Shop, \
    ProductImage, Tutorial, Makey
from models.like import LikeProductImage, LikeProduct, LikeProductDescription, \
    LikeShop, LikeProductTutorial, LikeMakey
from models.misc import EmailCollect


