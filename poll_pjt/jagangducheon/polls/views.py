from django.shortcuts import render, redirect, get_object_or_404
from .models import Poll, Comment
from .forms import PollForm, CommentForm
import random

# Create your views here.

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