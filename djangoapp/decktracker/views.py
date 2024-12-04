from .models import Deck
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return redirect('view_my_decks')

def view_my_decks(request):
    if not request.user.is_authenticated:
        return render(request, "login/login.html", {'error': 'You must be logged in to view your decks'})

    decks = Deck.objects.filter(owner=request.user)

    context = {
        'decks': decks,
        'authenticated': request.user.is_authenticated
    }

    return render(request, "decks/my_decks.html", context)

def view_deck(request, deck_id):
    deck_count = Deck.objects.filter(id=deck_id).count()

    if deck_count == 0:
        return HttpResponse(f"Deck {deck_id} not found")

    context = {
        'deck': Deck.objects.get(id=deck_id),
        'cards': list(Deck.objects.get(id=deck_id).get_cards()),
        'modifications': Deck.objects.get(id=deck_id).get_deck_modifications(),
        'card_count': sum([cd.quantity for cd in Deck.objects.get(id=deck_id).get_cards()]),
        'authenticated': request.user.is_authenticated
    }

    return render(request, "decks/deck.html", context)

def create_a_deck(request):
    if not request.user.is_authenticated:
        return render(request, "login/login.html", {'error': 'You must be logged in to create a deck'})

    if request.method == 'POST':
        if not request.POST['deck-name']:
            return render(request, "decks/new_deck.html", {'error': 'Deck name is required'})

        deck = Deck.objects.create(name=request.POST['deck-name'], owner=request.user)
        deck.save()

        return redirect('view_my_decks')

    return render(request, "decks/new_deck.html")

def remove_a_deck(request, deck_id):
    if not request.user.is_authenticated:
        return render(request, "login/login.html", {'error': 'You must be logged in to remove a deck'})

    if request.method == 'GET':
        if not deck_id:
            return render(request, "decks/my_decks.html", {'error': 'Deck ID is required'})

        deck = Deck.objects.filter(id=deck_id)

        if deck.count() == 0:
            return render(request, "decks/my_decks.html", {'error': 'Deck not found'})

        deck = list(deck)[0]

        if deck.owner != request.user:
            return render(request, "decks/my_decks.html", {'error': 'You do not own this deck'})

        deck.delete()

        return redirect('view_my_decks')

    return render(request, "decks/my_decks.html")

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
            return render(request, "login/login_form.html", {'error': 'Invalid username or password'})

        user = user[0]

        if user.check_password(password):
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return render(request, "login/login_form.html", {'success': 'Login Successful'})
            else:
                return render(request, "login/login_form.html", {'error': 'Invalid username or password'})
        else:
            return render(request, "login/login_form.html", {'error': 'Invalid username or password'})

    return render(request, "login/login.html")

def logout_view(request):
    logout(request)

    return render(request, "login/login.html", {'success': 'Logout Successful', 'logout': True})
