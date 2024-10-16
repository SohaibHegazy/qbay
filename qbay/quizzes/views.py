from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .forms import QuizForm, QuestionForm, AnswerFormSet
from .models import Quiz, Question, Answer, QuizAttempt


@login_required
def create_quiz(request):
    if request.method == 'POST':
        # Step 1: Create a quiz
        if 'quiz_form' in request.POST:
            quiz_form = QuizForm(request.POST)
            
            # Check if the title is unique
            if quiz_form.is_valid():
                title = quiz_form.cleaned_data.get('title')
                if Quiz.objects.filter(title=title).exists():
                    # If the quiz title already exists, show an error message
                    messages.error(request, 'A quiz with this title already exists. Please choose another title.')
                else:
                    quiz = quiz_form.save(commit=False)
                    quiz.created_by = request.user  # Link the quiz to the current user
                    quiz.is_published = False  # Ensure 'is_published' is set to False by default
                    quiz.save()

                    # Store quiz details in session
                    request.session['quiz_id'] = quiz.id  # Store quiz ID in session
                    request.session['questions_count'] = quiz.num_questions  # Store the number of questions
                    request.session['questions_added'] = 0  # Track added questions

                    # Redirect to the question form with the quiz_id as a parameter
                    return redirect('add_question', quiz_id=quiz.id)

        # Step 2: Add a question and its answers
        else:
            quiz_id = request.session.get('quiz_id')
            if quiz_id:
                quiz = get_object_or_404(Quiz, id=quiz_id)
                question_form = QuestionForm(request.POST)
                answer_formset = AnswerFormSet(request.POST)

                if question_form.is_valid() and answer_formset.is_valid():
                    # Save the question
                    question = question_form.save(commit=False)
                    question.quiz = quiz
                    question.save()

                    # Save the answers
                    answers = answer_formset.save(commit=False)
                    for answer in answers:
                        answer.question = question
                        answer.save()

                    # Update the session count for added questions
                    request.session['questions_added'] += 1

                    # Check if all questions have been added
                    if request.session['questions_added'] >= request.session['questions_count']:
                        return redirect('submit_quiz', quiz_id=quiz.id)  # Redirect to submit the quiz

                    return redirect('add_question', quiz_id=quiz.id)  # Redirect to add the next question

    else:
        quiz_form = QuizForm()

    return render(request, 'quizzes/create_quiz.html', {'quiz_form': quiz_form})


@login_required
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        answer_formset = AnswerFormSet(request.POST)

        if question_form.is_valid() and answer_formset.is_valid():
            # Save the question
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()

            # Save the answers
            answers = answer_formset.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()

            # Update the session count
            request.session['questions_added'] += 1

            # Check if the number of questions added is equal to the number entered
            if request.session['questions_added'] >= request.session['questions_count']:
                return redirect('submit_quiz', quiz_id=quiz.id)  # Redirect to submit quiz

            return redirect('add_question', quiz_id=quiz.id)  # Redirect to add the next question
    else:
        question_form = QuestionForm()
        answer_formset = AnswerFormSet(queryset=Answer.objects.none())

    return render(request, 'quizzes/add_question.html', {
        'quiz': quiz,
        'question_form': question_form,
        'answer_formset': answer_formset,
    })


@login_required
def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == 'POST':
        quiz.is_published = True  # Mark the quiz as published
        quiz.save()
        return redirect('quiz_list')  # Redirect to quiz list after submission

    return render(request, 'quizzes/submit_quiz.html', {'quiz': quiz})  # Render a confirmation template for submission


@login_required
def profile_view(request):
    """
    Display quizzes created by the logged-in user.
    """
    user_quizzes_created = Quiz.objects.filter(created_by=request.user)
    user_quizzes_taken = QuizAttempt.objects.filter(user=request.user)

    context = {
        'user_quizzes_created': user_quizzes_created,
        'user_quizzes_taken': user_quizzes_taken,

    }
    
    return render(request, 'profile.html', context)


@login_required
def delete_quiz(request, quiz_id):
    # Ensure the logged-in user is the creator of the quiz
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
    if request.method == 'POST':
        quiz.delete()
        return redirect('profile')  # Redirect to the profile after deletion
    return render(request, 'quizzes/delete_quiz.html', {'quiz': quiz})


@login_required
def available_quizzes(request):
    """
    View to display a list of all available quizzes as links.
    """
    quizzes = Quiz.objects.filter(is_published=True)

    return render(request, 'quizzes/available_quizzes.html', {'quizzes': quizzes})


@login_required
def take_quiz(request, quiz_id):
    """
    View to handle taking a specific quiz and submitting the answers.
    """
    quiz = get_object_or_404(Quiz, id=quiz_id, is_published=True)
    questions = Question.objects.filter(quiz=quiz)

    if request.method == 'POST':
        correct_count = 0
        total_questions = questions.count()

        for question in questions:
            selected_answer_id = request.POST.get(f'question_{question.id}')
            if selected_answer_id:
                selected_answer = Answer.objects.get(id=selected_answer_id)
                if selected_answer.is_correct:
                    correct_count += 1

        # Calculate the score
        score_percentage = (correct_count / total_questions) * 100

        # Save the attempt in the QuizAttempt model
        QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score_percentage
        )

        # Render the result page
        return render(request, 'quizzes/quiz_result.html', {
            'quiz': quiz,
            'correct_count': correct_count,
            'total_questions': total_questions,
            'score_percentage': score_percentage
        })

    # For GET requests, display the quiz form
    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'quizzes/take_quiz.html', context)


def quiz_detail(request, quiz_id):
    """
    View to display quiz details.
    """
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz, 'questions': questions})


def quiz_list(request):
    """
    View to display a list of published quizzes.
    """
    quizzes = Quiz.objects.filter(is_published=True)
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})
