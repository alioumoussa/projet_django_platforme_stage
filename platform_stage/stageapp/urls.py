from django.urls import path
from stageapp import views

app_name = "stageapp"


urlpatterns = [

    path('', views.home_view, name='home'),
    path('stages/', views.stage_list_View, name='stage-list'),
    path('stage/create/', views.create_stage_View, name='create-stage'),
    path('stage/<int:id>/', views.single_stage_view, name='single-stage'),
    path('apply-stage/<int:id>/', views.apply_stage_view, name='apply-stage'),
    path('bookmark-stage/<int:id>/', views.stage_bookmark_view, name='bookmark-stage'),
    path('about/', views.single_stage_view, name='about'),
    path('contact/', views.single_stage_view, name='contact'),
    path('result/', views.search_result_view, name='search_result'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/employer/stage/<int:id>/applicants/', views.all_applicants_view, name='applicants'),
    path('dashboard/employer/stage/edit/<int:id>', views.stage_edit_view, name='edit-stage'),
    path('dashboard/employer/applicant/<int:id>/', views.applicant_details_view, name='applicant-details'),
    path('dashboard/employer/close/<int:id>/', views.make_complete_stage_view, name='complete'),
    path('dashboard/employer/delete/<int:id>/', views.delete_stage_view, name='delete'),
    path('dashboard/student/delete-bookmark/<int:id>/', views.delete_bookmark_view, name='delete-bookmark'),


]
