from django.urls import path
from .views import dashboard, register, job_list, add_job, edit_job, delete_job, CustomLoginView, CustomLogoutView
from . import views

urlpatterns = [
    path("job_list/", job_list, name="job_list"),
    path('jobs/', job_list, name='job_list'),
    path("add/", add_job, name="add_job"),
    path("edit/<int:job_id>/", edit_job, name="edit_job"),
    path("delete/<int:job_id>/", delete_job, name="delete_job"),
    path("dashboard/", dashboard, name="dashboard"),
    path("register/", register, name="register"),
    path("", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),

    path('urgent-jobs/', views.urgent_jobs, name='urgent_jobs'),


]
