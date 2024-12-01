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

    def add_card(self, card, quantity):
        if CardDeck.objects.filter(card=card, deck=self).exists():
            cd = CardDeck.objects.get(card=card, deck=self)
            cd.quantity += quantity
            cd.save()
        else:
            CardDeck.objects.create(card=card, deck=self, quantity=quantity)

        DeckModification.objects.create(deck=self, card=card, quantity=-quantity)

    def add_cards(self, cards):

        for card, quantity in cards.items():
            self.add_card(card, quantity)

    def remove_card(self, card, quantity):
        cd = CardDeck.objects.get(card=card, deck=self)

        if cd.quantity <= quantity:
            cd.delete()
        else:
            cd.quantity -= quantity
            cd.save()

        DeckModification.objects.create(deck=self, card=card, quantity=-quantity)

    def remove_cards(self, cards):
        for card, quantity in cards.items():
            self.remove_card(card, quantity)

    def get_cards(self):
        return {cd for cd in CardDeck.objects.filter(deck=self)}

    def get_deck_modifications(self):
        # get results ordered by date
        # return DeckModification.objects.filter(deck=self).order_by('date')

        # group items by the second
        modifications = DeckModification.objects.filter(deck=self).order_by('date')

        # sort the modifications by date
        modifications = sorted(modifications, key=lambda x: x.date)

        # group the modifications by date
        grouped_modifications = {}

        for modification in modifications:
            date = modification.date.strftime("%Y-%m-%d sometime")

            # if morning
            if modification.date.hour < 12:
                date = modification.date.strftime("%Y-%m-%d morning")
            # if afternoon
            elif modification.date.hour < 18:
                date = modification.date.strftime("%Y-%m-%d afternoon")
            # if evening
            else:
                date = modification.date.strftime("%Y-%m-%d evening")

            if date not in grouped_modifications:
                grouped_modifications[date] = []

            grouped_modifications[date].append(modification)

        return grouped_modifications

class CardDeck(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.card.name} in {self.deck.name}'

    # on save, update the modification log
    def save(self, *args, **kwargs):
        super(CardDeck, self).save(*args, **kwargs)
        DeckModification.objects.create(deck=self.deck, card=self.card, quantity=self.quantity)

class DeckModification(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'Modification of deck \'{self.deck.name}\' on {self.date.strftime("%Y-%m-%d %H:%M:%S")}'

    # add calculated field 'added' to show if the card was added or removed
    @property
    def added(self):
        return self.quantity > 0
