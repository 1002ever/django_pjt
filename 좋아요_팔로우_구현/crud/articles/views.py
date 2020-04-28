from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .forms import ArticleForm


def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)

def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:index')
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/form.html', context)

def like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    user = request.user


    # add나 remove는 save까지 해주는 함수이므로 save 불필요
    if user in article.like_users.all():
    # if article.like_users.filter(id=user.id).exists():
    # 위와 동일한 검사 코드, but 아래가 더 빠름. python 함수가 아닌, 쿼리 자체 처리이므로.
        article.like_users.remove(user)
    else:
        article.like_users.add(user)
    return redirect('articles:index')
