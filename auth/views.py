from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


def password_changed(request):
    messages.add_message(request, messages.INFO, 'PASSWORD CHANGED SUCCESSFULLY')
    return redirect(reverse('profile:home'))
