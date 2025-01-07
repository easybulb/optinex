from django.shortcuts import render, redirect
from .models import Service, Appointment
from django.contrib import messages
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required

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


@login_required
def dashboard(request):
    # Get the logged-in user's appointments
    user_appointments = Appointment.objects.filter(email=request.user.email).order_by('date', 'time')
    return render(request, 'core/dashboard.html', {'appointments': user_appointments})


@login_required
def admin_dashboard(request):
    # Restrict access to staff (admin) users only
    if not request.user.is_staff:
        return redirect('account_dashboard')  # Redirect non-admin users to their dashboard
    return render(request, 'core/admin_dashboard.html')


@login_required
def role_based_redirect(request):
    # Redirect users based on their role
    if request.user.is_staff:  # Check if the user is a staff/admin
        return redirect('admin_dashboard')
    else:
        return redirect('account_dashboard')  # Redirect regular users to their dashboard
