from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Subject, Test, Question, Answer, StudentResult

class CustomUserAdmin(UserAdmin):
    # Add 'role' to the standard fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    # Add 'role' to the fields displayed on the user creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )
    # Add 'role' to the columns displayed in the user list
    list_display = ('username', 'email', 'role', 'is_staff', 'student_groups', 'student_password', 'student_full_name')
    # Add 'role' to the filters
    list_filter = UserAdmin.list_filter + ('role',)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    list_filter = ('created_at', 'created_by')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)


class TestAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'subject', 'created_by', 'status', 'total_time_minutes', 'created_at')
    list_filter = ('status', 'subject', 'created_by', 'created_at')
    search_fields = ('test_name', 'subject__name')
    readonly_fields = ('created_at', 'updated_at')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'test', 'question_type', 'points_value', 'created_at')
    list_filter = ('question_type', 'test', 'created_at')
    search_fields = ('question_text', 'test__test_name')
    readonly_fields = ('created_at',)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer_text', 'question', 'is_correct', 'created_at')
    list_filter = ('is_correct', 'question', 'created_at')
    search_fields = ('answer_text', 'question__question_text')
    readonly_fields = ('created_at',)


class StudentResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'test', 'score_achieved', 'total_score', 'time_taken', 'completion_date')
    list_filter = ('completion_date', 'student', 'test')
    search_fields = ('student__username', 'test__test_name')
    readonly_fields = ('completion_date',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(StudentResult, StudentResultAdmin)
