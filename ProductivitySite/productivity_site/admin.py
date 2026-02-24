from django.contrib import admin
from .models import User, FreeTime, Subject, Syllabus

# Register your models here.
admin.site.register(User)
admin.site.register(FreeTime)
admin.site.register(Subject)
admin.site.register(Syllabus)