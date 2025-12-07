from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Admin/Teacher Dashboard URLs
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    
    # Teacher URLs
    path('teacher/dashboard/', views.teacher_dashboard_view, name='teacher_dashboard'),
    path('teacher/test/create/', views.create_test_view, name='create_test'),
    
    # Student URLs
    path('student/dashboard/', views.student_dashboard_view, name='student_dashboard'),
    path('student/test/<int:test_id>/', views.take_test_view, name='take_test'),
    path('student/test/<int:test_id>/submit/', views.submit_test_view, name='submit_test'),
]