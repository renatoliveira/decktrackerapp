from django.http import HttpResponse
from django.shortcuts import render
from .models import Deck
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

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

def register_view(request):
    if request.method == 'POST':

        # make sure attributes are not empty
        if not request.POST['username'] or not request.POST['email'] or not request.POST['password']:
            return render(request, "registration/registration_form.html", {'error': 'All fields are required'})

        try:
            user = User.objects.create_user(
                request.POST['username'],
                request.POST['email'],
                request.POST['password']
            )

            user.save()
        except Exception as e:
            return render(request, "registration/registration_form.html", {'error': f'Error creating user'})

        return render(request, "registration/registration_form.html", {'success': 'Registration Successful'})

    else:
        return render(request, "registration/register.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.filter(username=username)

        if user.count() == 0:
            render(request, "registration/login.html", {'error': 'Invalid username or password'})

        user = user[0]

        if user.check_password(password):
            render(request, "registration/login.html", {'error': 'Invalid username or password'})
        else:
            render(request, "registration/login.html", {'error': 'Invalid username or password'})

    return render(request, "registration/login.html")
