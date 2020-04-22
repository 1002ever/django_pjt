from django.shortcuts import render, redirect, get_object_or_404
from .models import Review, Comment
from .forms import ReviewForm, CommentForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.
def review_list(request):
    reviews = Review.objects.all()
    context = {
        'reviews' : reviews
    }
    return render(request, 'community/review_list.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('community:detail', review.pk)
    else:
        form = ReviewForm()
    context ={
        'form': form
    }
    return render(request, 'community/form.html', context)

def detail(request, detail_pk):
    review = get_object_or_404(Review, pk = detail_pk)
    form = CommentForm()
    context = {
        'review': review,
        'form': form,
    }
    return render(request, 'community/review_detail.html', context)

@login_required
def update(request, detail_pk):
    review = get_object_or_404(Review, pk = detail_pk)
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect('community:detail', review.pk)
        else:
            form = ReviewForm(instance = review)
        context = {
            'form' : form
        }
        return render(request, 'community/form.html', context)
    else:
        return redirect('community:review_list')

@require_POST
@login_required
def delete(request, detail_pk):
    review = get_object_or_404(Review, pk = detail_pk)
    if request.user == review.user:
        review.delete()
    return redirect('community:review_list')

@login_required
def comment_create(request, detail_pk):
    review = get_object_or_404(Review, pk=detail_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form. save(commit=False)
            comment.user = request.user
            comment.review = review
            comment.save()
    return redirect('community:detail', review.pk)

@require_POST
def comment_delete(request,detail_pk ,comment_pk):
    if request.method == 'POST':
        comment = Comment.objects.get(pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('community:detail', detail_pk)
