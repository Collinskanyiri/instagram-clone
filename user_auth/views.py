from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from mainapp.models import *



def login_user(request):
    message='Instagram'
    if request.method== 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user =authenticate(username=username, password=password)
        
        if user is not None:
            login(request,user)
            messages.success(request, (f"welcome to Instagram"))
            return redirect('home')

        else:
            messages.success(request,("Something went wrong"))

            return render(request, 'authentication/login.html')
    else:

        return render(request, 'authentication/login.html', {"message": message})

def logout_user(request):
    logout(request)
    messages.success(request,("You have logged out"))
    return redirect('home')

def user_signup(request):
    message='Sign up to see photos and videos from your friends.'

    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']

            user = authenticate(username=username, password=password )
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request,("Account created successfully"))

            return redirect('home')
          
    else:
        form=UserCreationForm()
    return render(request,'authentication/signup.html', {"message":message, "form":form})
