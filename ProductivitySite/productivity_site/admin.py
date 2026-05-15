from django.contrib import admin

from productivity_site.models import *


@admin.register(FreeTime)
class FreeTimeAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    list_filter = ('user_id',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_id', 'user_id', 'name', 'description')
    list_filter = ('user_id',)
    search_fields = ('name', 'description')


@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ('syllabus_id', 'subject_id', 'order')
    list_filter = ('subject_id',)


@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ('summary_id', 'syllabus_id', 'name', 'formatted_text')
    list_filter = ('syllabus_id',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'subject_id', 'name', 'due_date', 'priority', 'estimated_time', 'text')
    list_filter = ('subject_id', 'priority', 'due_date')
    search_fields = ('name', 'text')


@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    list_display = ('subtask_id', 'task_id', 'name', 'due_date', 'priority', 'estimated_time', 'description')
    list_filter = ('task_id', 'priority', 'due_date')
    search_fields = ('name', 'description')


@admin.register(FillBlanks)
class FillBlanksAdmin(admin.ModelAdmin):
    list_display = ('fill_blanks_id', 'summary_id','text', 'hint', 'times_answered', 'times_correct')
    list_filter = ('summary_id',)


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('flashcard_id', 'summary_id', 'question', 'hint', 'times_answered', 'times_correct')
    list_filter = ('summary_id',)
    search_fields = ('question',)


@admin.register(Multioption)
class MultioptionAdmin(admin.ModelAdmin):
    list_display = ('multioption_id', 'summary_id', 'question', 'hint', 'times_answered', 'times_correct')
    list_filter = ('summary_id',)
    search_fields = ('question',)


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ('podcast_id', 'summary_id', 'text')
    list_filter = ('summary_id',)
