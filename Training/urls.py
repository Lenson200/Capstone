from django.urls import path
from django.conf.urls.static import static
from Training import views
urlpatterns = [
    path("",views.index,name="index"),
    path("login",views.login_view, name="login"),
    path("Register",views.register,name="register"),
    path("logout",views.logout_view, name="logout"),
    path("profileview", views.profile_view,name="profileview"),
]