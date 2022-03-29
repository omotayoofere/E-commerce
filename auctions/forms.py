from django.forms import ModelForm
from . import models

class AuctionForm(ModelForm):
    class Meta:
        model = models.Auction
        fields = "__all__"

    def xyz(self):
        pass