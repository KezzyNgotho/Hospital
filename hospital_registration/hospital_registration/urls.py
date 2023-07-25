from django.contrib import admin
from django.urls import path
from registration import views



urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("admin/login/", views.admin_login, name="admin_login"),
    path("admin/signup/", views.admin_signup, name="admin_signup"),
    path("incharge/signup/", views.incharge_signup, name="incharge_signup"),
    path("incharge/login/", views.incharge_login, name="incharge_login"),
    path("patient/registration/", views.patient_registration, name="patient_registration"),
    path("patient/attendance/", views.patient_attendance, name="patient_attendance"),
    path("patient/signin/inpatient/<str:student_number>/", views.inpatient_signin, name="inpatient_signin"),
    path("patient/signin/outpatient/<str:student_number>/", views.outpatient_signin, name="outpatient_signin"),
    path("patient/signup/", views.PatientSignup, name="patient_signup"),  # Updated function name
    path('patient_sign_out/', views.patient_sign_out, name='patient_sign_out'),
    path("patient/dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("incharge/dashboard/", views.incharge_dashboard, name="incharge_dashboard"),
    path("save_inpatient_details/", views.save_inpatient_details, name="save_inpatient_details"),
    path('patients/', views.patients_list_view, name='patients_list'),
    
]
