from django.shortcuts import render

# Create your views here.
def signup(request):
    return render(request,'users/registraion.html')

def user_login(request):
    return render(request, 'users/login.html')

def profile(request):
    return render(request, 'users/profile.html')

def user_logout(request):
    ...