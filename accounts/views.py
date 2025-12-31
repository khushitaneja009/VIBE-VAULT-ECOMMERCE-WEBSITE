from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def signup_view(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in!')
        return redirect('all_products')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'accounts/signup.html')

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'accounts/signup.html')

        # Check if email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return render(request, 'accounts/signup.html')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')

    return render(request, 'accounts/signup.html')

def login_view(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in!')
        return redirect('all_products')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            
            # Redirect to next page if available, otherwise to products
            next_url = request.GET.get('next', 'all_products')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password!')
            return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')

def logout_view(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(request, f'Goodbye, {username}! See you soon.')
    return redirect('login')
