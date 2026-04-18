from django import forms
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import CreateView, FormView
from django.urls import reverse_lazy

from .forms import ContactForm
from django.conf import settings
# Create your views here.

# ------------------ Landing page ------------------------
def home(request):
    """Home page view."""
    if request.user.is_authenticated:
        return redirect('productivity_site:dashboard')

    return render(request, 'unauthorized/landing/home.html')

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

# ------------------ Landing page ------------------------
class ContactView(FormView):
    form_class = ContactForm
    template_name = "unauthorized/landing/home.html"
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        subject = form.cleaned_data["subject"]
        message = form.cleaned_data["message"]

        full_message = (
            f"Received message below from {email}, {subject}\n"
            f"________________________\n\n"
            f"{message}"
        )
        send_mail(
            subject="Received contact form submission",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL],
        )
        return super().form_valid(form)
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
    return render(request, 'authorized/subjects.html')

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


