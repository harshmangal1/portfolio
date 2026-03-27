from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import ContactMessage
import urllib.request
import json


def verify_recaptcha(recaptcha_response):
    try:
        url = 'https://www.google.com/recaptcha/api/siteverify'
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        data_encoded = urllib.parse.urlencode(data).encode()
        req = urllib.request.Request(url, data=data_encoded)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        return result.get('success', False)
    except:
        return True


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message')
        recaptcha_response = request.POST.get('g-recaptcha-response')
        
        if hasattr(settings, 'RECAPTCHA_PRIVATE_KEY') and settings.RECAPTCHA_PRIVATE_KEY:
            if not verify_recaptcha(recaptcha_response):
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                return redirect('contact')
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        messages.success(request, 'Message sent successfully!')
        return redirect('contact')
    
    return render(request, 'contact/index.html', {
        'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY
    })
