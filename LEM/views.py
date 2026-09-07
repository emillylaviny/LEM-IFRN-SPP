from django.shortcuts import render
from .models import Card

def home(request):
    return render(request, 'LEM/home.html')

    card = Card.objects.all()

    return render(request, "LEM/home.html", {
        'card': card
    })

def login(request):
    return render(request, 'LEM/login.html')
