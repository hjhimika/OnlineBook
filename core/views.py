from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.http import HttpResponse
from .models import User, Book
from .forms import UserRegistrationForm, BookUploadForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_approved:
                login(request, user)
                return redirect('book_list')
            else:
                return HttpResponse("Your account is not approved yet.")
        else:
            return HttpResponse("Invalid credentials.")
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def book_list(request):
    books = Book.objects.filter(expiry_date__gt=timezone.now())
    return render(request, 'book_list.html', {'books': books})

@login_required
def book_view(request, book_id):
    book = Book.objects.get(id=book_id)
    if book.is_expired():
        return HttpResponse("This book is expired.")
    return render(request, 'book_view.html', {'book': book})

@login_required
@user_passes_test(lambda u: u.is_admin)
def book_upload(request):
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookUploadForm()
    return render(request, 'book_upload.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_admin)
def approve_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_approved = True
    user.save()
    return redirect('admin_panel')

@login_required
@user_passes_test(lambda u: u.is_admin)
def admin_panel(request):
    users = User.objects.filter(is_approved=False, is_admin=False)
    return render(request, 'admin_panel.html', {'users': users})