from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseNotAllowed


# Auth libraries here:
from django.contrib.auth import login , logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegistationForm

def register_page( request: HttpRequest):
    return render(request, "register.html", {"form": RegistationForm})

def register_view(request: HttpRequest):
    if request.method == "POST":
        form = RegistationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("auth_page")
        else: return redirect("register_page")
    return HttpResponseNotAllowed(["POST",])
def login_page(request:HttpRequest):
    if request.user.is_authenticated : return redirect("auth_page")
    return render(request, "register.html", {"form":AuthenticationForm,
                                            "button":"Login","action":"login-view"})

def login_view(request: HttpRequest):
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("auth_page")
        else: return redirect("login_page")
    return HttpResponseNotAllowed(["POST",])


def logout_view(request: HttpRequest):
    logout(request)
    return redirect("login_page")

@login_required
def auth_page(request:HttpRequest):
    return render(request, "auth.html", {"user":request.user})

# Create your views here.