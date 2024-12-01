from django.shortcuts import get_object_or_404
from Training.models import EmployeeProfile

def profile_context(request):
    if request.user.is_authenticated:
        try:
            profile = get_object_or_404(EmployeeProfile, user=request.user)
            return {'profile': profile}
        except EmployeeProfile.DoesNotExist:
            return {'profile': None}
    return {'profile': None}