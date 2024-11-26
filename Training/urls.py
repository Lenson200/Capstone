from django.urls import path
from django.conf.urls.static import static
from Training import views
urlpatterns = [
    path("",views.index,name="index"),
]