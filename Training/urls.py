from django.urls import path
from django.conf.urls.static import static
from Training import views

urlpatterns = [
    path('',views.index,name="index"),
    path('search/', views.search, name='search'),
    path("login",views.login_view, name="login"),
    path("Register",views.register,name="register"),
    path("logout",views.logout_view, name="logout"),
    path("profileview", views.profile_view,name="profileview"),
    path('addmodules/',views.training_module_create,name='addmodules'),
    path('add-completed-training/', views.add_completed_trainings, name='add_completed_training'),
    path('training-modules/', views.training_module_list, name='training_module_list'),
   path('training_module/<int:pk>/delete/', views.training_module_delete, name='training_module_delete'),
    path('training-modules/<int:pk>/', views.training_module_detail, name='training_module_detail'),
    path('update_trainings_required/', views.update_trainings_required, name='update_trainings_required'),
    path('completed-trainings/', views.view_completed_trainings, name='view_completed_trainings'),
    path('employee/<int:employee_id>/', views.employee_trainings, name='employee_trainings'),
    path('categories/',views.category_list, name='category_list'),
    path('category/<str:category>/', views.category_detail, name='category_detail'),
   path('toggle-training-status/', views.toggle_training_status, name='toggle_training_status'),
   path('get-training-status/<int:training_module_id>/', views.get_training_status, name='get_training_status'),

]