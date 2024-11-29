from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EmployeeProfile,Trainingsrequired

@receiver(post_save, sender=Trainingsrequired)
def update_employees_required_trainings(sender, instance, created, **kwargs):
    """
    Update required_trainings field in EmployeeProfile when a Trainingsrequired entry is added or updated.
    """
    if created or instance:  
        employees = EmployeeProfile.objects.filter(Facility=instance.facility)
        for employee in employees:
            employee.required_trainings = instance
            employee.save(update_fields=['required_trainings'])
            print(f"Updated {employee.name}'s required trainings to {instance.Category}")