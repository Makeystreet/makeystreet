from django.contrib import admin

from models.article import *
from models.core import *
from models.top import *
from models.misc import *
from models.like import *
from models.review import *
from models.forum import *
from models.issues import *

import reversion


class MakeyAdmin(reversion.VersionAdmin):
    pass

admin.site.register(UserProfile)
admin.site.register(ProductImage)
admin.site.register(Makey, MakeyAdmin)
admin.site.register(TextDocumentation)
# admin.site.register(Makey)
admin.site.register(Space)
admin.site.register(Inventory)
admin.site.register(Tutorial)
admin.site.register(Product)
admin.site.register(Shop)
admin.site.register(Location)
admin.site.register(ProductShopUrl)
admin.site.register(ProductDescription)
admin.site.register(ProductReview)
admin.site.register(ShopReview)
admin.site.register(Comment)
admin.site.register(Note)
admin.site.register(Documentation)
admin.site.register(Image)
admin.site.register(Issue)
admin.site.register(Video)
admin.site.register(ArticleTag)
admin.site.register(Article)
admin.site.register(ArticleEmail)
admin.site.register(Listing)
admin.site.register(NewProduct)
admin.site.register(Collection)

admin.site.register(TopProducts)
admin.site.register(TopMakeys)
admin.site.register(TopTutorials)
admin.site.register(TopUsers)
admin.site.register(TopShops)
admin.site.register(CfiStoreItem)
admin.site.register(LikeCfiStoreItem)

# admin.site.register(EmailCollect)
admin.site.register(ToIndexStore)
# admin.site.register(Like)
# admin.site.register(LikeProduct)
# admin.site.register(LikeProductImage)
# admin.site.register(LikeMakey)
# admin.site.register(LikeTutorial)
# admin.site.register(LikeShop)
# admin.site.register(LikeProductDescription)
admin.site.register(SearchLog)


admin.site.register(Question)
admin.site.register(Answer)
