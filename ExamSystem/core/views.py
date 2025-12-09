from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import CustomUser, Test, Subject, StudentResult, Question, Answer
from .decorators import role_required, redirect_based_on_role


def login_view(request):
    """
    Login view that handles authentication and redirects based on user role.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Redirect based on user role
            if user.role == 'Admin':
                return redirect('admindashboard')  # This will be defined in URLs
            elif user.role == 'Teacher':
                return redirect('teacher_dashboard')
            elif user.role == 'Student':
                return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'core/login.html')


@login_required
def logout_view(request):
    """
    Logout view
    """
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    """
    Generic dashboard view that redirects based on user role
    """
    user_role = request.user.role
    
    if user_role == 'Admin':
        return redirect('admindashboard')
    elif user_role == 'Teacher':
        return redirect('teacher_dashboard')
    elif user_role == 'Student':
        return redirect('student_dashboard')
    else:
        return redirect('login')


@role_required(['Admin', 'Teacher'])
def admin_dashboard_view(request):
    """
    Admin dashboard view - accessible by Admin and Teacher (for admin-like functions)
    """
    # Get statistics for the dashboard
    total_users = CustomUser.objects.count()
    total_tests = Test.objects.count()
    total_subjects = Subject.objects.count()
    total_results = StudentResult.objects.count()
    
    context = {
        'total_users': total_users,
        'total_tests': total_tests,
        'total_subjects': total_subjects,
        'total_results': total_results,
        'user_role': request.user.role
    }
    return render(request, 'core/admin_dashboard.html', context)


@role_required(['Teacher'])
def teacher_dashboard_view(request):
    """
    Teacher dashboard view
    """
    # Get tests created by this teacher
    teacher_tests = Test.objects.filter(created_by=request.user)
    
    # Get subjects created by this teacher
    teacher_subjects = Subject.objects.filter(created_by=request.user)
    
    context = {
        'tests': teacher_tests,
        'subjects': teacher_subjects,
        'user_role': request.user.role
    }
    return render(request, 'core/teacher_dashboard.html', context)


@role_required(['Student'])
def student_dashboard_view(request):
    """
    Student dashboard view
    """
    # Get available subjects and tests
    available_tests = Test.objects.filter(status='Published')
    
    # Get student's results
    student_results = StudentResult.objects.filter(student=request.user)
    
    context = {
        'available_tests': available_tests,
        'student_results': student_results,
        'user_role': request.user.role
    }
    return render(request, 'core/student_dashboard.html', context)


@role_required(['Teacher'])
def create_test_view(request):
    """
    View for creating a test with questions and answers
    """
    if request.method == 'POST':
        # Process form data to create test with questions and answers
        test_name = request.POST.get('test_name')
        subject_id = request.POST.get('subject')
        total_time = request.POST.get('total_time_minutes')
        status = request.POST.get('status', 'Draft')
        
        # Get subject object
        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            messages.error(request, 'Subject does not exist.')
            return redirect('create_test')
        
        # Create the test
        test = Test.objects.create(
            test_name=test_name,
            subject=subject,
            created_by=request.user,
            total_time_minutes=int(total_time),
            status=status
        )
        
        # Process questions and answers
        question_texts = request.POST.getlist('question_text')
        question_types = request.POST.getlist('question_type')
        points_values = request.POST.getlist('points_value')
        
        for i, question_text in enumerate(question_texts):
            if question_text.strip():  # Only create if question text is not empty
                from .models import Question, Answer # DIAGNOSTIC IMPORT
                question_type = question_types[i] if i < len(question_types) else 'MCQ'
                points_value = int(points_values[i]) if i < len(points_values) and points_values[i].isdigit() else 1
                
                question = Question.objects.create(
                    test=test,
                    question_text=question_text,
                    question_type=question_type,
                    points_value=points_value
                )
                
                # Process answers for this question
                answer_texts = request.POST.getlist(f'question_{i}_answer_text')
                is_correct_list = request.POST.getlist(f'question_{i}_is_correct')
                
                for j, answer_text in enumerate(answer_texts):
                    if answer_text.strip():  # Only create if answer text is not empty
                        is_correct = str(j) in is_correct_list  # Check if this answer is marked as correct
                        Answer.objects.create(
                            question=question,
                            answer_text=answer_text,
                            is_correct=is_correct
                        )
        
        messages.success(request, 'Test created successfully!')
        return redirect('teacher_dashboard')
    
    # For GET request, show the form
    subjects = Subject.objects.filter(created_by=request.user)  # Only subjects created by the teacher
    context = {
        'subjects': subjects,
        'user_role': request.user.role
    }
    return render(request, 'core/create_test.html', context)


@role_required(['Student'])
def take_test_view(request, test_id):
    """
    View for students to take a test
    """
    try:
        test = Test.objects.get(id=test_id, status='Published')  # Only published tests
    except Test.DoesNotExist:
        messages.error(request, 'Test does not exist or is not available.')
        return redirect('student_dashboard')
    
    # Get questions for the test (randomized order)
    from django.db.models import Q
    import random
    questions = list(test.questions.all())
    random.shuffle(questions)  # Randomize question order
    
    context = {
        'test': test,
        'questions': questions,
        'user_role': request.user.role
    }
    return render(request, 'core/take_test.html', context)


@role_required(['Student'])
def submit_test_view(request, test_id):
    """
    View to handle test submission and scoring
    """
    if request.method != 'POST':
        return redirect('student_dashboard')
    
    try:
        test = Test.objects.get(id=test_id, status='Published')
    except Test.DoesNotExist:
        messages.error(request, 'Test does not exist or is not available.')
        return redirect('student_dashboard')
    
    # Calculate score
    score = 0
    total_score = 0
    
    for question in test.questions.all():
        total_score += question.points_value
        selected_answer_id = request.POST.get(f'question_{question.id}')
        
        if selected_answer_id:
            try:
                selected_answer = Answer.objects.get(id=selected_answer_id, question=question)
                if selected_answer.is_correct:
                    score += question.points_value
            except Answer.DoesNotExist:
                pass  # Invalid answer ID, skip
    
    # Save the result
    from django.utils import timezone
    completion_time = request.POST.get('time_taken', 0)  # Time in seconds
    
    StudentResult.objects.create(
        student=request.user,
        test=test,
        score_achieved=score,
        total_score=total_score,
        time_taken=int(completion_time),
        completion_date=timezone.now()
    )
    
    messages.success(request, f'Test submitted successfully! Your score: {score}/{total_score}')
    return redirect('student_dashboard')
