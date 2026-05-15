from django.urls import path

from . import views

app_name = 'productivity_site'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('calendar', views.calendar, name='calendar'),
    path('subjects', views.subjects, name='subjects'),
    path('subjects/create', views.subject_create, name='subject_create'),
    path('subjects/<int:subject_id>', views.subject_read, name='subject_read'),
    path('subjects/<int:subject_id>', views.subject_read, name='task_read'),
    path('subjects/<int:subject_id>/tasks/create', views.task_create, name='task_create'),
    path('productivity', views.productivity, name='productivity'),
    path('profile', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]