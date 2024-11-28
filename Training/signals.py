from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EmployeeProfile

@receiver(post_save, sender=EmployeeProfile)
def update_employee_trainings(sender, instance, created, **kwargs):
    """Update the training requirements for the employee after saving their profile."""
    if not created:
        # Call the method to update the required trainings whenever facility is changed
        instance.update_trainings_required()