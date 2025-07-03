from django import forms

class LoginForm(forms.Form):
    USER_TYPE_CHOICES = [
        ('operational', 'Operational User'),
        ('client', 'Client User'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect, label="User Type")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

# Signup form
class SignupForm(forms.Form):
    USER_TYPE_CHOICES = [
        ('operational', 'Operational User'),
        ('client', 'Client User'),
    ]
    name = forms.CharField(label="Name", max_length=100)
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Phone", max_length=15)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect, label="User Type")

# Upload form for operational user
default_upload_field_help = "Upload a file or enter data."
class OperationalUploadForm(forms.Form):
    file = forms.FileField(label="Select file to upload", required=False, help_text=default_upload_field_help)
    data = forms.CharField(label="Or enter data", widget=forms.Textarea, required=False)
