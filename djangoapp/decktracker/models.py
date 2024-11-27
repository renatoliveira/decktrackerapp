from django.db import models

# Create your models here.
class Card(models.Model):
    sf_id = models.CharField(max_length=40)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Deck(models.Model):
    name = models.CharField(max_length=200)
    cards = models.ManyToManyField(Card, through='DeckCard')

    def __str__(self):
        return self.name

class CardDeck(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.card.name} in {self.deck.name}'
