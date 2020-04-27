from django import forms
from .models import Poll, Comment



class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = [
            'poll_subject',
            'question_a',
            'question_b',
        ]

GENIUS_CHOICE = [
    ('up', '위쪽'),
    ('down', '아래쪽'),
]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'choice',
            'writer',
            'content',
        ]
        widgets = {
            'choice': forms.RadioSelect(choices="GENIUS_CHOICE"),
        }