from django.shortcuts import get_object_or_404
from Training.models import EmployeeProfile


def profile_context(request):
    if request.user.is_authenticated:
        profile = EmployeeProfile.objects.filter(user=request.user).first()
        return {'profile': profile}
    return {'profile': None}