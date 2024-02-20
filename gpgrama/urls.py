from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin_profile', views.admin_profile, name="adminProfile"),
    path('update_admin', views.update_admin, name="updateAdmin"),
    path('createcandidate/', views.create_candidate,name="createcandidate"),
    path('candidate/<int:candidate_id>', views.candidate,name="candidate"),
    path('candidate/filter/', views.filter_candidate),
    path('candidate/pipeline_filter/', views.filter_pipeline_candidate),
    path('updatecandidate/<int:candidate_id>', views.update_candidate),
    path('deletecandidate/<int:candidate_id>', views.delete_candidate),
    path('create_HiringManager/', views.create_HiringManager),
    path('hm/<int:hm_id>', views.hm, name="hm"),
    path('update_HiringManager/<int:hm_id>', views.update_HiringManager, name="update_HiringManager"),
    path('delete_HiringManager/<int:hm_id>', views.delete_HiringManager),
    path('create_Hr/', views.create_Hr), 
    path('hr/<int:hr_id>', views.hr),
    path('update_Hr/<int:hr_id>', views.update_Hr, name="updateHR"),
    path('delete_Hr/<int:hr_id>', views.delete_Hr),
  	path('logout/', views.logoutUser, name="logout"),
    path('listCandidates/', views.list_candidates, name="list_candidates"),
    path('login/', views.login, name='login'),
    path('', views.homeTest, name="homeTest"),
    path('navbar', views.navbar),
    path('admin_form', views.update_admin),
    path('base', views.base, name='base'),
    path('list_hr', views.list_hr, name="list_hr"),
    path('list_hm', views.list_hm, name="list_hm"),
    path('pipeline', views.pipeline, name="pipeline"),
    path('manage_permissions', views.manage_permissions, name="manage_permissions")
]
