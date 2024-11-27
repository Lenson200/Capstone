from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from .models import EmployeeProfile

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