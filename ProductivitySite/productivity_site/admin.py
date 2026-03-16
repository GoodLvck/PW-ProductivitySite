from django.contrib import admin

from .models import User, Free_Time, Plan, Subject, Summary, Syllabus, Priority, Task, Subtask

admin.site.register(User)
admin.site.register(Free_Time)
admin.site.register(Plan)
admin.site.register(Subject)
admin.site.register(Summary)
admin.site.register(Syllabus)
admin.site.register(Priority)
admin.site.register(Task)
admin.site.register(Subtask)