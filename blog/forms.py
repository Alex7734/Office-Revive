from django import forms
from .models import Comment, Feedback


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class NewFeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['option', 'content']


class NewInviteForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["content"]