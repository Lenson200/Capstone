from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from PyPDF2 import PdfReader
from django.urls import reverse

# Create your models here.
User = get_user_model()

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_number =models.CharField(max_length=300)
    name = models.CharField(max_length=100)
    Team=models.CharField(max_length=100)
    designation=models.CharField(max_length=100,default="Technician")
    Facility=models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='Training/profile_pics', blank=True, null=True)
    required_trainings = models.ForeignKey('TrainingsRequired', on_delete=models.CASCADE, null=True, blank=True)  
    def is_manager(self):
        return any(keyword in self.designation.lower() for keyword in ['manager', 'reporting', 'Training Officer'])
    def is_reporting(self):
        return self.designation.lower() == 'Training Officer'

    def __str__(self):
      return f"{self.staff_number} - {self.name} {self.required_trainings}"

    def count_completed_trainings(self):
        """Returns the count of completed trainings employee."""
        return self.completed_trainings.filter(date_completed__isnull=False).count()
   
    
    def save(self, *args, **kwargs):
        # Automatically update required trainings based on Facility
        try:
            required_training = Trainingsrequired.objects.get(facility=self.Facility)
            self.required_trainings = required_training
        except Trainingsrequired.DoesNotExist:
            self.required_trainings = None

        super().save(*args, **kwargs)
        
class TrainingModule(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    code = models.CharField(max_length=10, unique=True)
    category = models.CharField(max_length=20, default="EQUIPMENT MANUAL")
    file = models.FileField(upload_to='Training/uploads/', blank=True, null=True)
    facility=models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_pages = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def update_total_pages(self):
        if self.file:
            with open(self.file.path, 'rb') as f:
                pdf_reader = PdfReader(f)
                self.total_pages = len(pdf_reader.pages)
                self.save()

    def get_absolute_url(self):
        return reverse('training_module_detail',args=[str(self.pk)])
    
class CompletedTraining(models.Model):
    employee = models.ForeignKey('EmployeeProfile', on_delete=models.CASCADE, related_name='completed_trainings')
    training_module = models.ForeignKey('TrainingModule', on_delete=models.CASCADE, related_name='completed_by_profiles')
    date_completed = models.DateTimeField(default=timezone.now)

    @property
    def date_of_expiry(self):
        """Return the expiry date as 2 years after the date completed."""
        return self.date_completed + timedelta(days=730) 

    class Meta:
        unique_together = ('employee', 'training_module')
        ordering = ['-date_completed']

        def __str__(self):
            return f"{self.employee.name} - {self.training_module.title}"
class Trainingsrequired(models.Model):
    facility = models.CharField(max_length=20)
    Required_Module_trainings = models.IntegerField(default=18)
    Category=models.CharField(max_length=50)

    def __str__(self):
        return f"Facility: {self.facility} - Required Trainings: {self.Required_Module_trainings}"
    