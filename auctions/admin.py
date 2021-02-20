from django.contrib import admin
from .models import User, Categories, Listing, watchlist, Bid, Comments

admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Listing)
admin.site.register(watchlist)
admin.site.register(Bid)
admin.site.register(Comments)
