from django.urls import path
from account import views

app_name = "account"

urlpatterns = [

    path('student/register/', views.employee_registration, name='student-registration'),
    path('employer/register/', views.employer_registration, name='employer-registration'),
    path('profile/edit/<int:id>/', views.employee_edit_profile, name='edit-profile'),
    path('upload-cv/', views.upload_cv, name='upload_cv'),
    path('view-cv/', views.view_cv, name='view_cv'),
    path('login/', views.user_logIn, name='login'),
    path('logout/', views.user_logOut, name='logout'),
]
