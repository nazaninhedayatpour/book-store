from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import login , authenticate , logout


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "accounts/register.html",
                {"error":"This username has already been taken"}
            )

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)
        return redirect("home")

    return render(request, "accounts/register.html")


def login_view(request):
    if request.method=="POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user=authenticate(
            request, 
            username=username,
            password=password
        )
        if user is not None:
            login(request,user)
            return redirect("home")
    else:
         return render(
                request,
                "accounts/login.html",
                {"error": "Username or password is incorrect."}
            )

    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect("home")


