from django.urls import path
from django.conf.urls.static import static
from Training import views
urlpatterns = [
    path("",views.index,name="index"),
    path("login",views.login_view, name="login"),
    path("Register",views.register,name="register"),
    path("logout",views.logout_view, name="logout"),
    path("profileview", views.profile_view,name="profileview"),
    path('addmodules',views.training_module_create,name='addmodules'),
    path('add-completed-training/', views.add_completed_trainings, name='add_completed_training'),
    path('employee/<int:employee_id>/', views.employee_trainings, name='employee_trainings'),
    path('training-modules/', views.training_module_list, name='training_module_list'),
    path('training-modules/<int:pk>/', views.training_module_detail, name='training_module_detail'),

]