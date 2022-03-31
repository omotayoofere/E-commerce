from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from . import models
from . import forms

class AuctionForm(ModelForm):
    class Meta:
        model = models.Auction
        exclude = ('current_price','created_by',)

    def xyz(self):
        pass


class BidForm(ModelForm):
    class Meta:
        model = models.Bid
        fields = ["bid_price",]

    def xyz(self):
        pass

class CommentForm(ModelForm):
    class Meta:
        model = models.Comment
        fields = ["comment"]


