from django.shortcuts import render, redirect

def login(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')