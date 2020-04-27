## \# 투표 기능 있는 페이지



\* 구현 사항

- 1:N 모델 만들기(Poll - Comment)
- forms.py에 choices 옵션 활용한 radioselect 사용
- 댓글 달기(삭제 없음)
- index 페이지는 Poll 중 랜덤으로 하나를 가져와 보여줌( + 댓글도 )



\*\* models.py

```python
from django.db import models

# Create your models here.

class Poll(models.Model):
    poll_subject = models.CharField(max_length=100)
    question_a = models.CharField(max_length=50)
    question_b = models.CharField(max_length=50)
    vote_a = models.IntegerField(default=0)
    vote_b = models.IntegerField(default=0)

class Comment(models.Model):
    GENIUS_CHOICES = [
        ('up', '위쪽'),
        ('down', '아래쪽'),
    ]
    choice = models.CharField(max_length=10, choices=GENIUS_CHOICES, blank=False, default='Unspecified')
    writer = models.CharField(max_length=100)
    content = models.TextField()
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

```



\*\* forms.py

```python
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
```



\*\* views.py

```python
from django.shortcuts import render, redirect, get_object_or_404
from .models import Poll, Comment
from .forms import PollForm, CommentForm
import random

# Create your views here.

# 이렇게 많은 연산이 들어가도 되는 건가?
def index(request):
    polls = Poll.objects.all()
    poll = random.choice(polls)
    comment = CommentForm()
    if poll.vote_a + poll.vote_b > 0:
        vote_rate_a = round(poll.vote_a/(poll.vote_a + poll.vote_b), 3) * 100
        vote_rate_b = round(poll.vote_b/(poll.vote_a + poll.vote_b), 3) * 100
    else:
        vote_rate_a = vote_rate_b = 0
    context = {
        'poll': poll,
        'comment': comment,
        'vote_rate_a': vote_rate_a,
        'vote_rate_b': vote_rate_b,
    }
    return render(request, 'polls/index.html', context)

def create(request):
    if request.method == "POST":
        form = PollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('polls:index')
    else:
        form = PollForm()
    context = {
        'form': form,
    }
    return render(request, 'polls/form.html', context)

def comment_create(request, poll_pk):
    poll = get_object_or_404(Poll, pk=poll_pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.poll = poll
            comment.save()
            if comment.choice == 'up':
                poll.vote_a += 1
            elif comment.choice == 'down':
                poll.vote_b += 1
            poll.save()
            return redirect('polls:index')
    else:
        form = CommentForm()
    context = {
        'form': form,
    }
    return render(request, 'polls/form.html', context)
```

