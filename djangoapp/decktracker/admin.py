from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Card)
admin.site.register(Deck)
admin.site.register(CardDeck)
admin.site.register(DeckModification)