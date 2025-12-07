from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Student')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.username} ({self.role})"


class Subject(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subjects_created')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name


class Test(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Published', 'Published'),
        ('Archived', 'Archived'),
    ]
    
    test_name = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='tests')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tests_created')
    total_time_minutes = models.IntegerField(default=60)  # Time in minutes
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.test_name


class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('MCQ', 'Multiple Choice'),
        ('TF', 'True/False'),
        ('ESSAY', 'Essay'),
    ]
    
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES, default='MCQ')
    points_value = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.question_text[:50]}..."


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.answer_text[:50]}... - Correct: {self.is_correct}"


class StudentResult(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='results')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results')
    score_achieved = models.FloatField(default=0.0)
    total_score = models.FloatField(default=0.0)
    time_taken = models.IntegerField()  # Time in seconds
    completion_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.student.username} - {self.test.test_name}: {self.score_achieved}/{self.total_score}"
