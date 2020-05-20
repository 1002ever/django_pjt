from django.shortcuts import render, redirect, get_object_or_404
from .models import Review, Movie, Comment
from .forms import ReviewForm, CommentForm
from django.contrib.auth.decorators import login_required

# 리뷰 대상 영화 표시 페이지
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'articles/index.html', context)

# 특정 영화에 해당되는 리뷰 페이지
def review_index(request, movie_pk):
    reviews = Review.objects.all().filter(movie_id=movie_pk)
    context = {
        'reviews': reviews,
        'movie_pk': movie_pk,
    }
    return render(request, 'articles/review_index.html', context)

# 로그인 된 사람만 글 작성 가능
@login_required
def create(request, movie_pk):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(pk=movie_pk)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect('articles:index')
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/review_form.html', context)

# 리뷰 상세 페이지
def detail(request, review_pk):
    review = Review.objects.get(id=review_pk)
    form = CommentForm()
    context = {
        'review': review,
        'form': form,
    }
    return render(request, 'articles/detail.html', context)

# detail 페이지에서의 좋아요 구현
@login_required
def like(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    user = request.user
    # 쿼리 질의로 속도 빠르게.
    if review.like_users.filter(id=user.id).exists():
        review.like_users.remove(user)
    else:
        review.like_users.add(user)
    return redirect('articles:detail', review.pk)

# update, delete는 로그인이 필요
# 작성자와 요청자가 같은지를 검사

@login_required
def update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if review.user == request.user:
        if request.method == "POST":
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
            # 수정을 성공하든, 못하든 일단 detail 페이지로.
            return redirect('articles:detail', review.pk)
        # POST 방식이 아니면 이전 데이터가 적힌 form 불러오기
        else:
            form = ReviewForm(instance=review)
        context = {
            'form': form,
        }
        return render(request, 'articles/review_form.html', context)
    # user 불일치 시 detail 페이지로
    else:
        return redirect('articles:detail', review.pk)

@login_required
def delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user:
        if request.method == "POST":
            review.delete()
        # 삭제가 성공하든, 실패하든 일단 review_index로
        return redirect('articles:review_index')
    # 유저 불일치 시 detail 페이지로
    else:
        return redirect('articles:detail', review.pk)

@login_required
def comment_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.review = review
            comment.save()
    return redirect('articles:detail', review.pk)

# 로그인 상태 & 유저 일치 시 댓글 삭제
@login_required
def comment_delete(request, review_pk, comment_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == "POST":
        comment = Comment.objects.get(pk=comment_pk)
        if request.user == review.user:
            comment.delete()
    return redirect('articles:detail', review.pk)