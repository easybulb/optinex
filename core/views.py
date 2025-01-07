from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, Appointment, Blog
from django.contrib import messages
from .forms import AppointmentForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.timezone import now

# Custom decorator for admin-only views
def admin_only(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

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
            form.save()
            messages.success(request, "Your appointment has been booked successfully!")
            return redirect('account_dashboard')
    else:
        form = AppointmentForm(user=request.user)
    return render(request, 'core/book_appointment.html', {'form': form})



@login_required
def cancel_appointment(request, appointment_id):
    # Get the appointment or return a 404 if it doesn't exist
    appointment = get_object_or_404(Appointment, id=appointment_id, email=request.user.email)
    if request.method == "POST":
        appointment.status = "Canceled"
        appointment.save()
        messages.success(request, "Your appointment has been canceled.")
        return redirect('account_dashboard')
    return render(request, 'core/confirm_cancel.html', {'appointment': appointment})


@login_required
def dashboard(request):
    # Filter appointments for the logged-in user
    user_appointments = Appointment.objects.filter(email=request.user.email).order_by('-date', '-time')

    # Separate upcoming and past appointments
    upcoming_appointments = user_appointments.filter(status__in=["Pending", "Confirmed"], date__gte=now())
    past_appointments = user_appointments.filter(status="Canceled", date__lt=now())

    # Calculate summary statistics
    total_appointments = user_appointments.count()
    active_appointments = upcoming_appointments.count()
    canceled_appointments = user_appointments.filter(status="Canceled").count()

    # Example notifications
    notifications = [
        "Check out our new blog post: '5 Tips for Healthy Vision!'",
        "Our new Quick Consultation service is now available!",
    ]

    # Handle profile update
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
    # Fetch all appointments for admin
    all_appointments = Appointment.objects.all().order_by('date', 'time')
    return render(request, 'core/admin_dashboard.html', {'appointments': all_appointments})


@login_required
def role_based_redirect(request):
    # Redirect users based on their role
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
        # Redirect to the blog list page
        return redirect('blog_list')
    return render(request, 'core/write_blog.html')


def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'core/blog_list.html', {'blogs': blogs})
