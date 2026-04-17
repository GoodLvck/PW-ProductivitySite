from django import forms


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
