from django import forms
from django.shortcuts import render
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.

def home(request):
    """Home page view."""
    return render(request, 'unauthorized/landing/home.html')

class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

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
