from django.shortcuts import render, redirect
from .models import Service
from django.contrib import messages
from .forms import AppointmentForm

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def services(request):
    services_list = Service.objects.all()
    return render(request, 'core/services.html', {'services': services_list})

def contact(request):
    return render(request, 'core/contact.html')

def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your appointment has been booked successfully!")
            return redirect('home')
    else:
        form = AppointmentForm()
    return render(request, 'core/book_appointment.html', {'form': form})


