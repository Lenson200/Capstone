from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login, logout
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from .models import User,EmployeeProfile,EmployeeProfile,CompletedTraining,TrainingModule,Trainingsrequired,Readdocuments
from django.db import IntegrityError
from django.http import JsonResponse
from .forms import EmployeeProfileForm,CompletedTrainingForm,TrainingModuleForm,TrainingsRequiredForm
from PyPDF2 import PdfReader
import os
from django.db.models import Q
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# Create your views here. none
def index(request):
    return render(request,'Training/index.html')

@login_required
def segregation(request):
    profile_instance = get_object_or_404(EmployeeProfile, user=request.user)
    return render(request, 'Training/Layout.html', {'profile': profile_instance})

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
        return HttpResponseRedirect(reverse("index"))
       
    else:
        return render(request, "Training/register.html")

def profile_view(request):
    user_instance = request.user
    try:
        # get employee profile for the current user
        profile_instance = EmployeeProfile.objects.get(user=user_instance)
    except EmployeeProfile.DoesNotExist:
       profile_instance = None
    
    completed_trainings_count = CompletedTraining.objects.filter(employee=profile_instance).count()
    read_modules_count = Readdocuments.objects.filter(employee=profile_instance, read_status=True).count()

    if request.method == "POST":
        form = EmployeeProfileForm(request.POST, request.FILES, instance=profile_instance)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = user_instance  
            new_profile.save() 
            return redirect('profileview')  
    else:
        form = EmployeeProfileForm(instance=profile_instance)

    context = {
        'profile': profile_instance,
        'completed_trainings_count': completed_trainings_count,
        'form': form,
        'read_modules_count': read_modules_count,
        'employee_id': profile_instance.id if profile_instance else 0 
    }

    # Render the profile page with the context
    return render(request, 'Training/profile.html', context)

#######################################Module creation,Deleteion,displaying and handling #####################
@login_required
def training_module_create(request):
    if request.method == 'POST':
        form = TrainingModuleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TrainingModuleForm()
    return render(request, 'Training/training_module_form.html', {'form': form})

def training_module_delete(request, pk):
    training_module = get_object_or_404(TrainingModule, pk=pk)

    if request.method == 'POST':
        training_module.delete()
        return redirect('index') 

    return render(request, 'Training/training_module_confirm_delete.html', {'training_module': training_module,})

def training_module_list(request):
    training_modules = TrainingModule.objects.all()
    return render(request, 'Training/training_module_list.html', {'training_modules': training_modules})

def training_module_detail(request, pk):
    training_module = get_object_or_404(TrainingModule, pk=pk)
    if training_module.file:
        file_extension = os.path.splitext(training_module.file.name)[1].lower()
        if file_extension == '.pdf':
            with open(training_module.file.path, 'rb') as f:
                pdf_reader = PdfReader(f)
                num_pages = len(pdf_reader.pages)

            if training_module.total_pages != num_pages:
                training_module.total_pages = num_pages
                training_module.save()

    return render(request, 'Training/training_module_detail.html', {
        'training_module': training_module,
        'page_range': range(1, training_module.total_pages + 1) if training_module.total_pages else None
    })
@login_required
def add_completed_trainings(request):
    if request.method == 'POST':
        form = CompletedTrainingForm(request.POST)
        if form.is_valid():
            employee = form.cleaned_data['employee_input']
            training_module = form.cleaned_data['training_module']
            date_completed = form.cleaned_data['date_completed']
            #before saving check if the record exists
            completed_training = CompletedTraining.objects.filter(
                employee=employee, training_module=training_module
            ).first()

            if completed_training:
                # Update the existing record 
                completed_training.date_completed = date_completed
                completed_training.save()
                form.add_error(
                    None, 
                    f'This employee has already completed this training module. The completion date has been updated to {date_completed}.'
                )
            else:
                # Create a new record
                completed_training = form.save(commit=False)
                completed_training.employee = employee
                completed_training.save()
                return redirect('add_completed_training')
    else:
        form = CompletedTrainingForm()
        context = {
        'form': form,
    }
    return render(request, 'Training/add_completed_training.html',context)


def employee_trainings(request, employee_id):
    if employee_id == 0:
        return redirect('profileview')
    employee = get_object_or_404(EmployeeProfile, pk=employee_id)
    completed_trainings = employee.completed_trainings.all()
    completed_trainings_count = employee.count_completed_trainings()
    
    return render(request, 'Training/Completed_training_details.html', {
        'employee': employee,
        'employee_id': employee_id,
        'completed_trainings': completed_trainings,

        })
@login_required
def update_trainings_required(request):
    if request.method == 'POST':
        form = TrainingsRequiredForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('index') 
    else:
        form = TrainingsRequiredForm()

    return render(request, 'Training/update_trainings_required.html', {'form': form})

#display a list of all available categories
def category_list(request):
    categories = TrainingModule.objects.values_list('category', flat=True).distinct()
    return render(request, 'Training/categories.html', {'categories': categories})

def category_detail(request, category):
    modules = TrainingModule.objects.filter(category__iexact=category)
    return render(request, 'Training/category_detail.html', {
        'category': category,
        'training_modules': modules
    })
@csrf_exempt
def toggle_training_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            training_module_id = data.get('training_module_id')
            employee = request.user.employeeprofile 

            
            try:
                readdocument = Readdocuments.objects.get(
                    employee=employee,
                    training_module_id=training_module_id
                )
                readdocument.read_status = not readdocument.read_status
                readdocument.save()

            except Readdocuments.DoesNotExist:
    
                readdocument = Readdocuments(
                    employee=employee,
                    training_module_id=training_module_id,
                    read_status=False  
                )
                readdocument.save()

            # Count how many training modules have been marked as "read" by the employee
            completed_count = Readdocuments.objects.filter(
                employee=employee,
                read_status=True
            ).count()

            return JsonResponse({
                'success': True,
                'new_status': readdocument.read_status,
                'completed_count': completed_count,
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)
def get_training_status(request, training_module_id):
    try:
        employee = request.user.employeeprofile
        read_status = Readdocuments.objects.get(
            employee=employee,
            training_module_id=training_module_id
        ).read_status
        return JsonResponse({
            'success': True,
            'read_status': read_status,
        })
    except Readdocuments.DoesNotExist:
        # If no record exists, assume the read_status is False
        return JsonResponse({
            'success': True,
            'read_status': False,
        })
    

    
def view_completed_trainings(request):
    employees=EmployeeProfile.objects.all().order_by('staff_number')
    return render(request, 'Training/staff_completed_trainings.html', {'employees': employees})   
def search(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        # Search in Profile, TrainingModule
        profile_results = EmployeeProfile.objects.filter(
            Q(name__icontains=query) | 
            Q(staff_number__icontains=query) | 
            Q(designation__icontains=query)
        )
        for profile in profile_results:
            results.append({
                'type': 'Profile',
                'name': profile.name,
                'description': profile.designation,
                'url': profile.get_absolute_url(), 
            })

    
        module_results = TrainingModule.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(code__icontains=query)
        )
        for module in module_results:
            results.append({
                'type': 'Training Module',
                'name': module.title,
                'description': module.description,
                'url': module.get_absolute_url(),  
            })
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
          return JsonResponse({'results': results}, safe=False)
    
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'Training/index.html', context)
