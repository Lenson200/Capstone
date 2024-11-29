from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from .models import EmployeeProfile,CompletedTraining,TrainingModule,Trainingsrequired
from django.db.models import Q

MAX_FILE_SIZE_MB = 6
class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ['name','staff_number', 'Team', 'designation', 'Facility', 'profile_pic']
    def clean_profile_pic(self):
        profile_pic = self.cleaned_data.get('profile_pic')
        
        # Check if the file size is within the limit (6MB)
        if profile_pic and profile_pic.size > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise ValidationError(f"File size must be less than {MAX_FILE_SIZE_MB} MB")
        
        return profile_pic

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add a file extension validator to the profile_pic field
        self.fields['profile_pic'].validators.append(
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
        )
class TrainingModuleForm(forms.ModelForm):
    class Meta:
        model = TrainingModule
        fields = ['title', 'description', 'file','code','category','facility']

    def clean_file(self):
        file = self.cleaned_data.get('file', False)
        if file:
            if file.size > 20*2024*2024:
                raise forms.ValidationError("File size must be under 20MB.")
            if not file.content_type in ['application/pdf', 'application/msword', 'application/vnd.ms-excel', 'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.openxmlformats-officedocument.presentationml.presentation']:
                raise forms.ValidationError("File type is not supported.")
            return file
        
class CompletedTrainingForm(forms.ModelForm):
    employee_input = forms.CharField(
        required=True,
        label="Employee",
        widget=forms.TextInput(attrs={'placeholder': 'Type employee staff number or name ...'})
    )

    class Meta:
        model = CompletedTraining
        fields = ['training_module', 'date_completed']
        widgets = {
            'date_completed': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_employee_input(self):
        employee_input = self.cleaned_data.get('employee_input').strip()
        print(f"Input received: '{employee_input}'")
        try:
            employee = EmployeeProfile.objects.get(
                Q(name__iexact=employee_input) | Q(staff_number__iexact=employee_input)
            )
            return employee
        except EmployeeProfile.DoesNotExist:
            print("Exact match not found, attempting partial match.")
            try:
                employee = EmployeeProfile.objects.get(
                    Q(name__icontains=employee_input) | Q(staff_number__icontains=employee_input)
                )
                return employee
            except EmployeeProfile.DoesNotExist:
                print("No matching employee found.")
                raise forms.ValidationError("No matching employee found. Please check the input.")

class TrainingsRequiredForm(forms.ModelForm):
    class Meta:
        model = Trainingsrequired
        fields = ['facility', 'Required_Module_trainings','Category'] 
        widgets = {
            'facility': forms.TextInput(attrs={'class': 'form-control'}),
            'required_module_trainings': forms.NumberInput(attrs={'class': 'form-control'}),
            'Category': forms.TextInput(attrs={'class': 'form-control'}),
           
        }