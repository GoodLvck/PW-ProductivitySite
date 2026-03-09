from django.contrib import admin

from django.contrib import admin
from .models import User, Free_Time, Plan, Subject, Summary, Syllabus

admin.site.register(User)
admin.site.register(Free_Time)
admin.site.register(Plan)
admin.site.register(Subject)
admin.site.register(Summary)
admin.site.register(Syllabus)