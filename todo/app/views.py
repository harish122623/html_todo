from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from app.models import Todo
from django.contrib import messages

# Home view (protected)
@login_required(login_url='/login')
def home_view(request):
    return render(request, 'signup.html')


# Signup View
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('fnm')
        email = request.POST.get('email')
        password = request.POST.get('pwd')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('/signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, 'Account created successfully. Please login.')
        return redirect('/login')

    return render(request, 'signup.html')


# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('fnm')
        password = request.POST.get('pwd')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/todopage')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('/login')

    return render(request, 'login.html')


# Todo View (Add & List)
@login_required(login_url='/login')
def todo_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Todo.objects.create(title=title, user=request.user)
            messages.success(request, 'Todo added successfully.')
        return redirect('/todopage')

    todos = Todo.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html', {'res': todos})


# Delete Todo View
@login_required(login_url='/login')
def delete_todo_view(request, srno):
    todo = get_object_or_404(Todo, srno=srno, user=request.user)
    todo.delete()
    messages.success(request, 'Todo deleted successfully.')
    return redirect('/todopage')


# Edit Todo View
@login_required(login_url='/login')
def edit_todo_view(request, srno):
    todo = get_object_or_404(Todo, srno=srno, user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            todo.title = title
            todo.save()
            messages.success(request, 'Todo updated successfully.')
        return redirect('/todopage')

    return render(request, 'edit.html', {'obj': todo})


# Logout View
@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('/login')
