from django.shortcuts import render
from .models import Card

def home(request):
    return render(request, 'app/home.html')

    card = Card.objects.all()

    return render(request, "app/home.html", {
        'card': card
    })

def login(request):
    return render(request, 'app/login.html')
