from django import forms
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.mail import BadHeaderError
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from django.db.models import Count
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import ContactForm, SubjectForm, TaskForm, SubtaskForm
from django.conf import settings

from .models import Subject, Task, subject, Subtask


def _set_pending_subtasks_count(tasks):
    task_ids = [task.task_id for task in tasks]
    pending_counts = {
        item["task_id"]: item["count"]
        for item in Subtask.objects.filter(
            task_id__in=task_ids,
            completed=False,
        ).values("task_id").annotate(count=Count("subtask_id"))
    }

    for task in tasks:
        task.pending_subtasks_count = pending_counts.get(task.task_id, 0)


def _subtask_list_context(task, subject):
    subtasks = Subtask.objects.filter(
        task_id=task,
    ).order_by("completed", "due_date")

    return {
        "task": task,
        "subject": subject,
        "subtasks": subtasks,
        "pending_subtasks": subtasks.filter(completed=False),
    }


# ------------------ Landing page ------------------------
def home(request):
    if request.user.is_authenticated:
        return redirect('productivity_site:dashboard')

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            full_message = (
                f"New contact form submission\n\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Subject: {subject}\n\n"
                f"Message:\n{message}"
            )

            try:
                send_mail(
                    subject=f"[ZenOrbit Contact] {subject}",
                    message=full_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.NOTIFY_EMAIL],
                )
            except BadHeaderError:
                messages.error(
                    request,
                    "The message could not be sent because the headers are invalid.",
                )
            except Exception:
                messages.error(
                    request,
                    "We could not send your message right now. Please try again later.",
                )
            else:
                messages.success(request, "Your message has been sent successfully.")
                return redirect('productivity_site:home')
    else:
        form = ContactForm()

    return render(request, 'unauthorized/landing/home.html', {'form': form})



# ------------------ Log in page ------------------------
class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'superzen01'
        self.fields['password'].widget.attrs['placeholder'] = 'password123'

class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = CustomLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("productivity_site:dashboard")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Log in"
        context["form_subtitle"] = "Welcome back to ZenOrbit"
        context["submit_label"] = "Log in"
        return context

# ------------------ Register page ------------------------
class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'field-sm'
        self.fields['last_name'].widget.attrs['class'] = 'field-sm'

        self.fields['first_name'].widget.attrs['placeholder'] = 'Your name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Your surname'
        self.fields['username'].widget.attrs['placeholder'] = 'superzen01'
        self.fields['email'].widget.attrs['placeholder'] = 'your@email.com'
        self.fields['password1'].widget.attrs['placeholder'] = 'At least 8 characters'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user

class SignUpView(CreateView):
    """Register view."""
    form_class = CustomRegisterForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("productivity_site:dashboard")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Sign Up"
        context["form_subtitle"] = "Create your ZenOrbit account"
        context["submit_label"] = "Create account"
        return context

# ------------------ Change password page ------------------------


# ------------------ Dashboard page ------------------------
@login_required
def dashboard(request):
    return render(request, 'authorized/dashboard.html')

# ------------------ Calendar page ------------------------
@login_required
def calendar(request):
    return render(request, 'authorized/calendar.html')

# ------------------ Subjects page ------------------------
@login_required
def subjects(request):
    subjects = Subject.objects.filter(user_id=request.user)

    return render(request, "authorized/subjects/subjects.html", {
        "subjects": subjects,
    })

@login_required
def subject_create(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)

        if form.is_valid():
            subject = form.save(commit=False)
            subject.user_id = request.user
            subject.save()
            return redirect("productivity_site:subjects")
    else:
        form = SubjectForm()

    return render(request, "authorized/create.html", {
        "form": form,
        "form_title": "Create subject",
        "form_subtitle": "Add a subject to organize your tasks and study material.",
        "submit_label": "Create subject",
        "cancel_url": reverse("productivity_site:subjects"),
    })

@login_required
def subject_read(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id, user_id=request.user)

    pending_tasks = list(Task.objects.filter(
        subject_id=subject,
        completed=False,
    ))

    completed_tasks = list(Task.objects.filter(
        subject_id=subject,
        completed=True,
    ))

    _set_pending_subtasks_count(pending_tasks)

    return render(request, "authorized/subjects/subject_view.html", {
        "subject": subject,
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks,
    })

@login_required
def task_toggle_completed(request, subject_id, task_id):
    task = get_object_or_404(
        Task,
        task_id=task_id,
        subject_id__subject_id=subject_id,
        subject_id__user_id=request.user,
    )

    if request.method == "POST":
        task.completed = not task.completed
        task.save(update_fields=["completed"])

        if task.completed:
            Subtask.objects.filter(
                task_id=task,
                completed=False,
            ).update(completed=True)

    return redirect("productivity_site:subject_read", subject_id=subject_id)

@login_required
def subject_update(request, subject_id):
    subject = get_object_or_404(
        Subject,
        subject_id=subject_id,
        user_id=request.user,
    )

    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect("productivity_site:subject_read", subject_id=subject.subject_id)
    else:
        form = SubjectForm(instance=subject)

    return render(request, "authorized/create.html", {
        "form": form,
        "form_title": "Edit subject",
        "form_subtitle": "Update this subject.",
        "submit_label": "Save changes",
        "cancel_url": reverse("productivity_site:subject_read", args=[subject.subject_id]),
    })

@login_required
def subject_delete(request, subject_id):
    subject = get_object_or_404(
        Subject,
        subject_id=subject_id,
        user_id=request.user,
    )

    if request.method == "POST":
        subject.delete()
        return redirect("productivity_site:subjects")

    return render(request, "authorized/delete.html", {
        "object_name": subject.name,
        "object_type": "subject",
        "cancel_url": reverse("productivity_site:subject_read", args=[subject.subject_id]),
    })

# ------------------ Task create page ------------------------
@login_required
def task_create(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id, user_id=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.subject_id = subject
            task.save()

            return redirect(
                "productivity_site:subject_read",
                subject_id=subject.subject_id,
            )
    else:
        form = TaskForm()

    return render(request, "authorized/create.html", {
        "form": form,
        "form_title": "Create task",
        "form_subtitle": f"Add a task to {subject.name}.",
        "submit_label": "Create task",
        "cancel_url": reverse(
            "productivity_site:subject_read",
            args=[subject.subject_id],
        ),
    })

def task_read(request, subject_id, task_id):
    task = get_object_or_404(Task, pk=task_id, subject_id=subject_id)
    subject = get_object_or_404(Subject, pk=subject_id, user_id=request.user)

    context = _subtask_list_context(task, subject);

    return render(request, "authorized/tasks/task_view.html", context)

@login_required
def task_update(request, subject_id, task_id):
    task = get_object_or_404(
        Task,
        task_id=task_id,
        subject_id__subject_id=subject_id,
        subject_id__user_id=request.user,
    )

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(
                "productivity_site:task_read",
                subject_id=subject_id,
                task_id=task.task_id,
            )
    else:
        form = TaskForm(instance=task)

    return render(request, "authorized/create.html", {
        "form": form,
        "form_title": "Edit task",
        "form_subtitle": f"Update {task.name}.",
        "submit_label": "Save changes",
        "cancel_url": reverse("productivity_site:task_read", args=[subject_id, task.task_id]),
    })


@login_required
def task_delete(request, subject_id, task_id):
    task = get_object_or_404(
        Task,
        task_id=task_id,
        subject_id__subject_id=subject_id,
        subject_id__user_id=request.user,
    )

    if request.method == "POST":
        task.delete()
        return redirect("productivity_site:subject_read", subject_id=subject_id)

    return render(request, "authorized/delete.html", {
        "object_name": task.name,
        "object_type": "task",
        "cancel_url": reverse("productivity_site:task_read", args=[subject_id, task.task_id]),
    })


# ------------------ Subtask create page ------------------------
@login_required
def subtask_create(request, subject_id, task_id):
    task = get_object_or_404(
        Task,
        task_id=task_id,
        subject_id__subject_id=subject_id,
        subject_id__user_id=request.user,
    )

    if request.method == "POST":
        form = SubtaskForm(request.POST)

        if form.is_valid():
            subtask = form.save(commit=False)
            subtask.task_id = task
            subtask.save()

            if task.completed:
                task.completed = False
                task.save()

            return redirect(
                "productivity_site:task_read",
                subject_id=subject_id,
                task_id=task.task_id,
            )
    else:
        form = SubtaskForm()

    return render(request, "authorized/create.html", {
        "form": form,
        "form_title": "Create subtask",
        "form_subtitle": f"Add a subtask to {task.name}.",
        "submit_label": "Create subtask",
        "cancel_url": reverse(
            "productivity_site:task_read",
            args=[subject_id, task.task_id],
        ),
    })

@login_required
def subtask_read(request, subject_id, task_id, subtask_id):
    subtask = get_object_or_404(
        Subtask,
        subtask_id=subtask_id,
        task_id__task_id=task_id,
        task_id__subject_id__subject_id=subject_id,
        task_id__subject_id__user_id=request.user,
    )

    task = subtask.task_id
    subject = task.subject_id

    return render(request, "authorized/subtasks/subtask_view.html", {
        "subject": subject,
        "task": task,
        "subtask": subtask,
    })

@login_required
def subtask_update(request, subject_id, task_id, subtask_id):
    subtask = get_object_or_404(
        Subtask,
        subtask_id=subtask_id,
        task_id__task_id=task_id,
        task_id__subject_id__subject_id=subject_id,
        task_id__subject_id__user_id=request.user,
    )

    if request.method == "POST":
        form = SubtaskForm(request.POST, instance=subtask)
        if form.is_valid():
            form.save()
            return redirect(
                "productivity_site:subtask_read",
                subject_id=subject_id,
                task_id=task_id,
                subtask_id=subtask.subtask_id,
            )
    else:
        form = SubtaskForm(instance=subtask)

    return render(request, "authorized/create.html", {
        "form": form,
        "form_title": "Edit subtask",
        "form_subtitle": f"Update {subtask.name}.",
        "submit_label": "Save changes",
        "cancel_url": reverse("productivity_site:subtask_read", args=[subject_id, task_id, subtask.subtask_id]),
    })

@login_required
def subtask_toggle_completed(request, subject_id, task_id, subtask_id):
    subtask = get_object_or_404(
        Subtask,
        subtask_id=subtask_id,
        task_id__task_id=task_id,
        task_id__subject_id__subject_id=subject_id,
        task_id__subject_id__user_id=request.user,
    )

    if request.method == "POST":
        task = subtask.task_id
        subtask.completed = not subtask.completed

        if not subtask.completed and task.completed:
            task.completed = False

        subtask.save(update_fields=["completed"])
        task.save(update_fields=["completed"])

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        task = subtask.task_id
        subject = task.subject_id
        if request.headers.get("x-subtask-detail") == "true":
            return render(request, "authorized/subtasks/_subtask_status.html", {
                "subject": subject,
                "task": task,
                "subtask": subtask,
            })

        return render(
            request,
            "authorized/tasks/_subtask_list.html",
            _subtask_list_context(task, subject),
        )

    referer_url = request.META.get("HTTP_REFERER")
    if referer_url and url_has_allowed_host_and_scheme(
        url=referer_url,
        allowed_hosts={request.get_host()},
    ):
        return redirect(referer_url)

    return redirect(
        "productivity_site:task_read",
        subject_id=subject_id,
        task_id=task_id,
    )

@login_required
def subtask_delete(request, subject_id, task_id, subtask_id):
    subtask = get_object_or_404(
        Subtask,
        subtask_id=subtask_id,
        task_id__task_id=task_id,
        task_id__subject_id__subject_id=subject_id,
        task_id__subject_id__user_id=request.user,
    )

    if request.method == "POST":
        subtask.delete()
        return redirect(
            "productivity_site:task_read",
            subject_id=subject_id,
            task_id=task_id,
        )

    return render(request, "authorized/delete.html", {
        "object_name": subtask.name,
        "object_type": "subtask",
        "cancel_url": reverse("productivity_site:subtask_read", args=[subject_id, task_id, subtask.subtask_id]),
    })


# ------------------ Productivity page ------------------------
@login_required
def productivity(request):
    return render(request, 'authorized/productivity.html')

# ------------------ Profile page ------------------------
@login_required
def profile(request):
    return render(request, 'authorized/profile.html')

# ------------------ Logout route ------------------------
@login_required
def logout_view(request):
    logout(request)
    return redirect("productivity_site:home")
