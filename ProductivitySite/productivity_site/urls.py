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
    path("subjects/<int:subject_id>/update", views.subject_update, name="subject_update"),
    path("subjects/<int:subject_id>/delete", views.subject_delete, name="subject_delete"),
    path('subjects/<int:subject_id>/tasks/create', views.task_create, name='task_create'),
    path('subjects/<int:subject_id>/tasks/<int:task_id>', views.task_read, name='task_read'),
    path("subjects/<int:subject_id>/tasks/<int:task_id>/update", views.task_update, name="task_update"),
    path("subjects/<int:subject_id>/tasks/<int:task_id>/delete", views.task_delete, name="task_delete"),
    path('subjects/<int:subject_id>/tasks/<int:task_id>/subtasks/create', views.subtask_create, name='subtask_create'),
    path('subjects/<int:subject_id>/tasks/<int:task_id>/subtasks/<int:subtask_id>', views.subtask_read, name='subtask_read'),
    path("subjects/<int:subject_id>/tasks/<int:task_id>/subtasks/<int:subtask_id>/update", views.subtask_update, name="subtask_update"),
    path("subjects/<int:subject_id>/tasks/<int:task_id>/subtasks/<int:subtask_id>/delete", views.subtask_delete, name="subtask_delete"),

    path('productivity', views.productivity, name='productivity'),
    path('profile', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]