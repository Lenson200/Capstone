from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login, logout
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from .models import User,EmployeeProfile,EmployeeProfile,CompletedTraining
from django.db import IntegrityError
from django.http import JsonResponse
from .forms import EmployeeProfileForm,CompletedTrainingForm,TrainingModuleForm


# Create your views here.
def index(request):
    return render(request,'Training/index.html')

###########################ACCOUNT REGISTRATION AND PROFILE HANDLING############################
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check for AJAX request
                return JsonResponse({"success": True, "message": "Login successful."})
            return redirect(next_url if next_url else 'index')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check for AJAX request
                return JsonResponse({"success": False, "message": "Invalid username and/or password."})
            return render(request, 'Training/login.html', {
                "message": "Invalid username and/or password.",
                "next": request.GET.get("next"),
            })
    else:
        return render(request, "Training/login.html", {"next": request.GET.get("next")})
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password=request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "Training/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "Training/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return render(request, "Training/register.html", {
            "message": "Registration successful! You are now logged in."
        })
    else:
        return render(request, "Training/register.html")

def profile_view(request):
    user_instance = request.user
    try:
        # get employee profile for the current user
        profile_instance = EmployeeProfile.objects.get(user=user_instance)
    except EmployeeProfile.DoesNotExist:
        raise Http404("Profile not found.")
    
    completed_trainings_count = CompletedTraining.objects.filter(employee=profile_instance).count()
    if request.method == "POST":
        form = EmployeeProfileForm(request.POST, request.FILES, instance=profile_instance)
        if form.is_valid():
            form.save() 
            return redirect('profileview')  
    else:
        form = EmployeeProfileForm(instance=profile_instance)

    context = {
        'profile': profile_instance,
        'completed_trainings_count': completed_trainings_count,
        'form': form,
    }

    # Render the profile page with the context
    return render(request, 'Training/profile.html', context)
def add_completed_trainings(request):
    if request.method == 'POST':
        form = CompletedTrainingForm(request.POST)


def training_module_create(request):
    if request.method == 'POST':
        form = TrainingModuleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TrainingModuleForm()
    return render(request, 'Training/training_module_form.html', {'form': form})
