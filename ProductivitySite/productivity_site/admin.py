from django.contrib import admin

from productivity_site.models import User, Free_Time, Plan, Subject, Summary, Syllabus, Fill_Blanks, Flashcard, Multioption, Priority, Task, Subtask

admin.site.register(User)
admin.site.register(Free_Time)
admin.site.register(Plan)
admin.site.register(Subject)
admin.site.register(Summary)
admin.site.register(Syllabus)
admin.site.register(Priority)
admin.site.register(Task)
admin.site.register(Subtask)
admin.site.register(Fill_Blanks)
admin.site.register(Flashcard)
admin.site.register(Multioption)