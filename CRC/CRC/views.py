from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm, OperationalUploadForm
from django.contrib import messages
from django.http import HttpResponse
from .models import UploadedFile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
import os
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired

signer = TimestampSigner()

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data['user_type']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on user_type
                if user_type == 'operational':
                    return redirect('operational_dashboard')
                elif user_type == 'client':
                    return redirect('client_dashboard')
                else:
                    messages.error(request, 'Invalid user type.')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            user_type = form.cleaned_data['user_type']
            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
            else:
                if User.objects.filter(username=email).exists():
                    messages.error(request, 'A user with this email already exists.')
                else:
                    user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
                    user.save()
                    # Optionally, save phone and user_type in user profile or a custom model
                    messages.success(request, 'Account created successfully! Please log in.')
                    return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def operational_dashboard(request):
    if request.method == 'POST':
        form = OperationalUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data.get('file')
            entered_data = form.cleaned_data.get('data')
            if uploaded_file:
                # Save file to database
                file_content = uploaded_file.read()
                UploadedFile.objects.create(
                    file=uploaded_file,  # Optional: keep file on disk
                    file_content=file_content,
                    file_name=uploaded_file.name,
                    uploaded_by=request.user
                )
                messages.success(request, 'File uploaded successfully!')
            elif entered_data:
                # Optionally, save entered data as a file or another model
                messages.success(request, 'Data submitted successfully!')
            else:
                messages.error(request, 'Please upload a file or enter data.')
            return redirect('operational_dashboard')
    else:
        form = OperationalUploadForm()
    return render(request, 'operational_dashboard.html', {'form': form})

@login_required
def client_dashboard(request):
    uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    files = []
    if os.path.exists(uploads_dir):
        for filename in os.listdir(uploads_dir):
            file_path = os.path.join('uploads', filename)
            files.append({
                'name': filename,
                'url': settings.MEDIA_URL + 'uploads/' + filename
            })
    files = sorted(files, key=lambda x: x['name'], reverse=True)
    return render(request, 'client_dashboard.html', {'files': files})

def splash_view(request):
    return render(request, 'splash.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def generate_download_link(request, filename):
    # Only allow client users
    if not hasattr(request.user, 'is_authenticated') or not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    # You may want to check user type here if you store it in a profile
    # For now, assume all authenticated users are clients
    # If you have a user_type field, check it here
    # Example: if request.user.profile.user_type != 'client':
    #     return HttpResponse('Forbidden', status=403)
    token = signer.sign(filename)
    url = request.build_absolute_uri(reverse('secure_download', args=[token]))
    return HttpResponse(url)

@login_required
def secure_download(request, token):
    try:
        filename = signer.unsign(token, max_age=300)  # Link valid for 5 minutes
    except (BadSignature, SignatureExpired):
        return HttpResponse('Invalid or expired link', status=403)
    # Check user type here as above
    # Example: if request.user.profile.user_type != 'client':
    #     return HttpResponse('Forbidden', status=403)
    uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    file_path = os.path.join(uploads_dir, filename)
    if not os.path.exists(file_path):
        return HttpResponse('File not found', status=404)
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
