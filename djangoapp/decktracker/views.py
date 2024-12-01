from django.http import HttpResponse
from django.shortcuts import render
from .models import Deck

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the decktracker index.")

def view_deck(request, deck_id):
    deck_count = Deck.objects.filter(id=deck_id).count()

    if deck_count == 0:
        return HttpResponse(f"Deck {deck_id} not found")

    context = {
        'deck': Deck.objects.get(id=deck_id),
        'cards': list(Deck.objects.get(id=deck_id).get_cards()),
        'modifications': Deck.objects.get(id=deck_id).get_deck_modifications(),
        'card_count': sum([cd.quantity for cd in Deck.objects.get(id=deck_id).get_cards()])
    }

    return render(request, "decks/deck.html", context)
