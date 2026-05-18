from django import forms
from django.utils import timezone

from productivity_site.models import Subject, Task, Subtask


class ContactForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Name", "class": "form-field"}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "E-mail", "class": "form-field"}
        )
    )
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Subject", "class": "form-field"}
        )
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Your message...", "class": "form-field"}
        )
    )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        return email

class SubjectForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user is not None:
            self.instance.user_id = user

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not self.user:
            return name

        duplicate = Subject.objects.filter(user_id=self.user, name__iexact=name)
        if self.instance.pk:
            duplicate = duplicate.exclude(pk=self.instance.pk)
        if duplicate.exists():
            raise forms.ValidationError("A subject with that name already exists")
        return name

    class Meta:
        model = Subject
        fields = ["name", "description", "color"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Subject name",
                    "class": "form-field",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Describe what you will study in this subject...",
                    "class": "form-field",
                    "rows": 5,
                }
            ),
            "color": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-field color-field",
                }
            ),
        }

class TaskForm(forms.ModelForm):
    def __init__(self, *args, subject=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.subject = subject
        if subject is not None:
            self.instance.subject_id = subject

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not self.subject:
            return name

        duplicate = Task.objects.filter(subject_id=self.subject, name__iexact=name)
        if self.instance.pk:
            duplicate = duplicate.exclude(pk=self.instance.pk)
        if duplicate.exists():
            raise forms.ValidationError("A task with that name already exists")
        return name

    def clean_due_date(self):
        due_date = self.cleaned_data["due_date"]
        if due_date < timezone.now():
            raise forms.ValidationError("Due date cannot be in the past")
        return due_date

    def clean_estimated_time(self):
        estimated_time = self.cleaned_data["estimated_time"]
        if estimated_time <= 0:
            raise forms.ValidationError("Estimated time must be greater than 0")
        return estimated_time

    class Meta:
        model = Task
        fields = ["name", "text", "due_date", "priority", "estimated_time"]

        labels = {
            "name": "Task name",
            "text": "Description",
            "due_date": "Due date",
            "priority": "Priority",
            "estimated_time": "Estimated time",
        }

        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Task name", "class": "form-field"}),
            "text": forms.Textarea(attrs={"placeholder": "Describe the task...", "class": "form-field", "rows": 5}),
            "due_date": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-field datetime-field"}),
            "priority": forms.Select(attrs={"class": "form-field select-field"}),
            "estimated_time": forms.NumberInput(attrs={"placeholder": "Minutes", "class": "form-field", "min": 1}),
        }

class SubtaskForm(forms.ModelForm):
    def __init__(self, *args, task=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.task = task
        if task is not None:
            self.instance.task_id = task

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not self.task:
            return name

        duplicate = Subtask.objects.filter(task_id=self.task, name__iexact=name)
        if self.instance.pk:
            duplicate = duplicate.exclude(pk=self.instance.pk)
        if duplicate.exists():
            raise forms.ValidationError("A subtask with that name already exists")
        return name

    def clean_due_date(self):
        due_date = self.cleaned_data["due_date"]
        if due_date < timezone.now():
            raise forms.ValidationError("Due date cannot be in the past")
        if self.task and due_date > self.task.due_date:
            raise forms.ValidationError("Subtask due date cannot be after the task due date")
        return due_date

    def clean_estimated_time(self):
        estimated_time = self.cleaned_data["estimated_time"]
        if estimated_time <= 0:
            raise forms.ValidationError("Estimated time must be greater than 0")
        return estimated_time

    class Meta:
        model = Subtask
        fields = ["name", "description", "due_date", "priority", "estimated_time"]

        labels = {
            "name": "Subtask name",
            "description": "Description",
            "due_date": "Due date",
            "priority": "Priority",
            "estimated_time": "Estimated time",
        }

        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Subtask name", "class": "form-field"}),
            "description": forms.Textarea(attrs={"placeholder": "Describe the subtask...", "class": "form-field", "rows": 5}),
            "due_date": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-field datetime-field"}),
            "priority": forms.Select(attrs={"class": "form-field select-field"}),
            "estimated_time": forms.NumberInput(attrs={"placeholder": "Minutes", "class": "form-field", "min": 1}),
        }
