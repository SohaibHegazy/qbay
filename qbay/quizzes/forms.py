from django import forms
from .models import Quiz, Question, Answer

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'num_questions']
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Quiz.objects.filter(title=title).exists():
            raise forms.ValidationError('A quiz with this title already exists. Please choose another title.')
        return title

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']


AnswerFormSet = forms.modelformset_factory(Answer, fields=('text', 'is_correct'), extra=4)
