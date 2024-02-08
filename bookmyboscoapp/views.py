from django.shortcuts import get_object_or_404, redirect, render,redirect
from adminboscoapp.models import *
from bookmyboscoapp.models import *
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# ... other imports ...

import math
import queue
import random
from django.contrib.auth import logout as django_logout
import random
from django.http import HttpResponse
from django.contrib.auth import login
from decimal import Decimal
from django.contrib.auth import authenticate


import string
from django.views.decorators.cache import cache_control

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout as django_logout
from django.shortcuts import get_object_or_404
import time
import stripe
from django.conf import settings
from django.db.models import Q
from twilio.rest import Client
from django.http import JsonResponse
from django.contrib import messages
# Other necessary imports...

# Home view
def home(request):
    distinct_movie_names = Movie.objects.order_by('movie_name').values_list('movie_name', flat=True).distinct()
    movies = [Movie.objects.filter(movie_name=name).first() for name in distinct_movie_names]
    return render(request, 'index.html', {'movies': movies})

# Movie details view
def movie_details(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    cinemas = Shows.objects.filter(movie=movie).select_related('theater_name')
    return render(request, 'moviedetails.html', {'movie': movie, 'cinemas': cinemas})

# User registration view
def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(username=username, email=email, first_name=firstname, last_name=lastname)
        user.set_password(password)
        user.save()

        return redirect('login_user')

    return render(request, 'userregister.html')

# Generate OTP
def generate_otp():
    return str(random.randint(1000, 9999))

# Send OTP
def send_otp(phone_number, otp):
    try:
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=f'Your OTP is: {otp}',
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
    except Exception as e:
        print(f"Error sending OTP: {e}")

# Login view
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
    if user is not None:
        auth_login(request, user)
        movie_id = request.session.get('movie_id_for_booking', None)
        if movie_id:
            return redirect('movie_details', movie_id=movie_id)
        return redirect('home')
    else:
        return render(request, 'login.html', {'error': 'Invalid username or password.'})

    return render(request, 'login.html')

# Verify OTP
def verify_otp(request):
    # OTP verification logic...
    # Similar to your existing implementation
    pass

# Seat selection view
def seat(request, movie_id):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, id=movie_id)
        # Additional logic if needed
        return render(request, 'seat.html', {'movie': movie})
    else:
        return redirect('login_user')

# Ticket view
def ticket(request):
    return render(request, 'ticket.html')

# User logout view
def user_logout(request):
    auth_logout(request)
    return redirect('home')

# Theater list view
def theater_list(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    theaters_showing_movie = Shows.objects.filter(movie_show__movie=movie).select_related('theater_name')
    return render(request, 'theatre.html', {'movie': movie, 'theaters': theaters_showing_movie})