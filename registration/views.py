# registration/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from twilio.rest import Client
from django.conf import settings
from .forms import CustomUserCreationForm, OTPVerificationForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data['phone_number']
            generate_and_send_otp(request, user, phone_number)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def otp_verification(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            user = CustomUser.objects.get(username=request.user.username)
            if otp == user.otp:
                user.otp_verified = True
                user.save()
                login(request, user)
                return redirect('profile')
    else:
        form = OTPVerificationForm()
    return render(request, 'registration/otp_verification.html', {'form': form})

@login_required
def profile(request):
    # Your profile view logic goes here
    return render(request, 'registration/profile.html')

def generate_and_send_otp(request, user, phone_number):
    otp = generate_random_otp()
    user.otp = otp
    user.save()
    message = f'Your OTP is: {otp}'
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        message = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
    except Exception as e:
        # Handle Twilio exceptions
        pass

import random

def generate_random_otp():
    # Generate a 6-digit OTP
    otp = ''.join(random.choice('0123456789') for _ in range(6))
    return otp
