from django.test import TestCase
from decktracker.models import *

class DeckSetupTestCase(TestCase):
    def setUp(self):
        Deck.objects.create(name='Test Deck')
        Card.objects.create(sf_id='1', name='Test Card')

    def test_add_card_to_deck(self):
        deck = Deck.objects.get(name='Test Deck')
        card = Card.objects.get(name='Test Card')
        deck.add_card(card, 1)

        self.assertEqual(CardDeck.objects.get(card=card, deck=deck).quantity, 1)
        self.assertEqual(DeckModification.objects.filter(deck=deck, card=card).count(), 1)

    def test_remove_card_from_deck(self):
        deck = Deck.objects.get(name='Test Deck')
        card = Card.objects.get(name='Test Card')
        deck.add_card(card, 1)
        deck.remove_card(card, 1)

        self.assertFalse(CardDeck.objects.filter(card=card, deck=deck).exists())
        self.assertEqual(DeckModification.objects.filter(deck=deck, card=card).count(), 2)

    def test_add_multiple_cards_to_deck(self):
        deck = Deck.objects.get(name='Test Deck')
        card = Card.objects.get(name='Test Card')
        deck.add_card(card, 1)
        deck.add_card(card, 2)

        self.assertEqual(CardDeck.objects.get(card=card, deck=deck).quantity, 3)
        self.assertEqual(DeckModification.objects.filter(deck=deck, card=card).count(), 2)

    def test_remove_multiple_cards_from_deck(self):
        deck = Deck.objects.get(name='Test Deck')
        card = Card.objects.get(name='Test Card')
        deck.add_card(card, 3)
        deck.remove_card(card, 2)

        self.assertEqual(CardDeck.objects.get(card=card, deck=deck).quantity, 1)
        self.assertEqual(DeckModification.objects.filter(deck=deck, card=card).count(), 2)