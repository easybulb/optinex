from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, Appointment, Blog
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import AppointmentForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q, Count
from django.utils.timezone import now
from django.db.models.functions import TruncMonth

# Custom decorator for admin-only views
def admin_only(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@login_required
@admin_only
def user_profile_from_appointment(request, appointment_id):
    # Get the appointment based on the id
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Use the appointment details to fetch all related appointments by the same user
    appointments = Appointment.objects.filter(email=appointment.email)

    return render(request, 'core/user_profile.html', {
        'user_info': appointment,  # Use the current appointment as user reference
        'appointments': appointments,  # List of all appointments for this user
    })



def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def services(request):
    services_list = Service.objects.all()
    return render(request, 'core/services.html', {'services': services_list})

def contact(request):
    return render(request, 'core/contact.html')

@login_required
def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():
            appointment = form.save(commit=False)
            # Save the full name (first and last name) of the user
            appointment.name = f"{request.user.first_name} {request.user.last_name}".strip()
            appointment.email = request.user.email  # Ensure email is set correctly
            appointment.save()
            messages.success(request, "Your appointment has been booked successfully!")
            return redirect('account_dashboard')
    else:
        form = AppointmentForm(user=request.user)
    return render(request, 'core/book_appointment.html', {'form': form})


from django.http import JsonResponse

@login_required
@admin_only
def get_appointment_details(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return JsonResponse({
        "id": appointment.id,
        "name": appointment.name,
        "email": appointment.email,
        "phone_number": appointment.phone_number,
        "service": appointment.service,
        "date": appointment.date.isoformat(),
        "time": appointment.time.isoformat(),
    })

@login_required
@admin_only
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == "POST":
        data = request.POST
        appointment.name = data.get("name", appointment.name)
        appointment.service = data.get("service", appointment.service)
        appointment.date = data.get("date", appointment.date)
        appointment.time = data.get("time", appointment.time)
        appointment.save()

        return JsonResponse({"success": True, "message": "Appointment updated successfully!"})

    return JsonResponse({"success": False, "message": "Invalid request."})



@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, email=request.user.email)
    if request.method == "POST":
        appointment.status = "Canceled"
        appointment.save()
        messages.success(request, "Your appointment has been canceled.")
        return redirect('account_dashboard')
    return render(request, 'core/confirm_cancel.html', {'appointment': appointment})

@login_required
def dashboard(request):
    user_appointments = Appointment.objects.filter(email=request.user.email).order_by('-date', '-time')
    upcoming_appointments = user_appointments.filter(status__in=["Pending", "Confirmed"], date__gte=now())
    past_appointments = user_appointments.filter(status="Canceled", date__lt=now())

    total_appointments = user_appointments.count()
    active_appointments = upcoming_appointments.count()
    canceled_appointments = user_appointments.filter(status="Canceled").count()

    notifications = [
        "Check out our new blog post: '5 Tips for Healthy Vision!'",
        "Our new Quick Consultation service is now available!",
    ]

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('account_dashboard')  # Refresh the dashboard
    else:
        user_form = UserUpdateForm(instance=request.user)

    return render(request, 'core/dashboard.html', {
        'user_form': user_form,
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        'total_appointments': total_appointments,
        'active_appointments': active_appointments,
        'canceled_appointments': canceled_appointments,
        'notifications': notifications,
    })

@login_required
@admin_only
def admin_dashboard(request):
    query = request.GET.get('q', '')
    appointments = Appointment.objects.filter(
        Q(name__icontains=query) | Q(email__icontains=query) | Q(service__icontains=query)
    ).order_by('-date', '-time')

    appointment_summary = Appointment.objects.aggregate(
        total=Count('id'),
        pending=Count('id', filter=Q(status="Pending")),
        confirmed=Count('id', filter=Q(status="Confirmed")),
        canceled=Count('id', filter=Q(status="Canceled"))
    )

    monthly_appointments = Appointment.objects.annotate(month=TruncMonth('date')).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    notifications = [
        "New feature: Subadmin management is now available!",
        "System maintenance scheduled for next week.",
    ]

    return render(request, 'core/admin_dashboard.html', {
        'appointments': appointments,
        'appointment_summary': appointment_summary,
        'monthly_appointments': monthly_appointments,
        'query': query,
        'notifications': notifications
    })

@login_required
@admin_only
def add_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment added successfully!")
            return redirect('admin_dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'core/add_appointment.html', {'form': form})

@login_required
@admin_only
def manage_users(request):
    users = User.objects.all()
    return render(request, 'core/manage_users.html', {'users': users})

@login_required
@admin_only
def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, f"User {user.email} has been deactivated.")
    return redirect('manage_users')

@login_required
def role_based_redirect(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    else:
        return redirect('account_dashboard')

@login_required
@admin_only
def write_blog(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        Blog.objects.create(title=title, content=content)
        messages.success(request, "Blog post created successfully!")
        return redirect('blog_list')
    return render(request, 'core/write_blog.html')

def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'core/blog_list.html', {'blogs': blogs})
