from django.contrib import admin
from .models import User, Listing, Category, Comment, Bid


class ListingAdmin(admin.ModelAdmin):
  list_display = ("id", "title", "is_active", "initial_bid", "creating_date", "won_bid", "closing_date")

  def won_bid(self, obj):
    highest_bid = obj.bids.order_by('bid').last()

    return highest_bid.bid if highest_bid else 'No bids'

  won_bid.short_description = "Won Bid"

# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Bid)
