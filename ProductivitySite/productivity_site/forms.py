from django import forms

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
            "due_date": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-field"}),
            "estimated_time": forms.NumberInput(attrs={"placeholder": "Minutes", "class": "form-field", "min": 1}),
        }

class SubtaskForm(forms.ModelForm):
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
            "due_date": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-field"}),
            "estimated_time": forms.NumberInput(attrs={"placeholder": "Minutes", "class": "form-field", "min": 1}),
        }