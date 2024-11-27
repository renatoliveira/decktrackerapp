from django.db import models

# Create your models here.
class Card(models.Model):
    sf_id = models.CharField(max_length=40)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Deck(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class CardDeck(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.card.name} in {self.deck.name}'

class DeckModification(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)

    def __str__(self):
        return f'Modification of deck {self.deck.name} on {self.date}'

class DeckModificationCard(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    deck_modification = models.ForeignKey(DeckModification, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.card.name} in {self.deck_modification.deck.name} on {self.deck_modification.date}'
