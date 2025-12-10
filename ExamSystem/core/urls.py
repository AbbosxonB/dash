from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Admin/Teacher Dashboard URLs
    path('admindashboard/', views.admin_dashboard_view, name='admindashboard'),
    path('export-results/', views.export_student_results_xls, name='export_student_results'),
    path('export-results-csv/', views.export_student_results_csv, name='export_student_results_csv'),
    path('result/<int:result_id>/delete/', views.delete_student_result_view, name='delete_student_result'),
    path('result/<int:result_id>/retake/', views.retake_test_view, name='retake_test'),
    
    # Teacher URLs
    path('teacher/dashboard/', views.teacher_dashboard_view, name='teacher_dashboard'),
    path('teacher/test/create/', views.create_test_view, name='create_test'),
    path('teacher/test/import/', views.import_test_view, name='import_test'),
    path('teacher/test/import/sample/', views.download_sample_excel, name='download_sample_excel'),
    path('teacher/test/<int:test_id>/edit/', views.edit_test_view, name='edit_test'),
    path('teacher/test/<int:test_id>/delete/', views.delete_test_view, name='delete_test'),
    
    # Student URLs
    path('student/dashboard/', views.student_dashboard_view, name='student_dashboard'),
    path('student/test/<int:test_id>/', views.take_test_view, name='take_test'),
    path('student/test/<int:test_id>/submit/', views.submit_test_view, name='submit_test'),
]