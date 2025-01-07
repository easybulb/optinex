from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('dashboard/', views.dashboard, name='account_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('role-redirect/', views.role_based_redirect, name='role_based_redirect'),
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('write-blog/', views.write_blog, name='write_blog'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-appointment/', views.add_appointment, name='add_appointment'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('deactivate-user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),

]
