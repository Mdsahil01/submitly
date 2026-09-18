from django.urls import path
from . import views

urlpatterns = [
    path('', views.root_view, name='root'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_redirect_view, name='dashboard_redirect'),
    path('student/dashboard/', views.student_dashboard_view, name='student_dashboard'),
    path('faculty/dashboard/', views.faculty_dashboard_view, name='faculty_dashboard'),
]
