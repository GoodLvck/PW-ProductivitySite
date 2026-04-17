from django.urls import path

from . import views

app_name = 'productivity_site'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('calendar', views.calendar, name='calendar'),
    path('subjects', views.subjects, name='subjects'),
    path('productivity', views.productivity, name='productivity'),
    path('profile', views.profile, name='profile'),
    path('accounts/logout', views.logout_view, name='logout'),
]