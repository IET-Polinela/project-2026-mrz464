from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CitizenRegistrationForm

def register_view(request):
    if request.method == "POST":
        form = CitizenRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_admin = False  # Memastikan yang daftar otomatis jadi Citizen 
            user.save()
            messages.success(request, f"Akun {user.username} berhasil dibuat! Silakan login.")
            return redirect("login")
    else:
        form = CitizenRegistrationForm()
    return render(request, "usermanagement_24782086/register.html", {"form": form})