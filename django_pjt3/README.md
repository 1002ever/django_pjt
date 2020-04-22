## \# 구현 사항



\* **<u>*실제 코드 구현 순서*</u>**

   리뷰 게시판(dummy) 작성

   => 회원가입, 로그인 구현

   => 리뷰 작성, 리뷰 게시판 구현

   => 리뷰 수정, 리뷰 삭제 구현

   => 로그아웃 구현(네비게이션 바 부분 완성 - `로그인/로그아웃 상태에 따라 다르게 보이게끔`)

   => 댓글 작성 / 삭제 구현

   => 네비게이션 바 완성(리뷰게시판, 새 글 쓰기 탭 추가)



\* **<u>*앱 별 기능 및 상세 구현 과정*</u>**

- accounts

  - 회원가입

  - 로그인

  - 로그아웃

    - 장고 내 User 모델을 이용 => 모델과 폼을 직접 정의해주지 않아도 된다는 특징

    - login, logout 을 import 하는 경우, 함수명인 login, logout과 겹쳐 재귀가 발생

      => login, logout을 각각 auth_login, auth_logout 으로 지정

    - login_required 는 필요 함수 위에 @login_required를 명시

      => 로그인 되지 않은 상태로 해당 함수에 접근하면, login 페이지로 redirect 한다.

    ```python
    # accounts 폴더 내 views.py 의 import 내역

    from django.shortcuts import render, redirect
    from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
    from django.contrib.auth import login as auth_login
    from django.contrib.auth import logout as auth_logout
    from django.contrib.auth.decorators import login_required
    ```



- community

  - 리뷰 게시판(index 페이지 역할 + 새 글 쓰기 버튼)

    - Review 모델, ReviewForm 폼을 각각 명세대로 정의

    - python manage.py makemigrations / python manage.py migrate 로 적용

    - Review.objects.all() 을 통해 모두 불러온 후 html 문서에서 for문으로 나열

    - 새 글 쓰기 버튼

      ㄱ. @login_required 검사

      ㄴ. POST 방식이면 request.POST를 form에 할당하여 저장 후 detail 페이지로 redirect

      ㄷ. POST 방식이 아니면 빈 폼을 form에 할당하여 html에 전달

  - 리뷰 상세 페이지(detail 페이지)

    - get_object_or_404(Review, pk=detail_pk) 를 이용하여 review를 지정
    - 그 attribute들을 html 문서 내에서 보여줌

  - 리뷰 수정 / 삭제(detail 페이지 내부에 기능 구현)

    - 둘 다 @login_required를 필요로 함

    - 삭제의 경우 POST 방식으로 진행했으므로, @require_POST가 추가적으로 필요

    - 수정과 삭제는 form.html을 공유

      => 폼의 내용이 다를 뿐, 폼을 전부 열거하여 보여준다는 점은 같기 때문

    ** 수정

    ​	ㄱ. get_object_or_404(Review, pk=detail_pk) 를 통해 review를 할당

    ​	ㄴ. 수정 전 수정을 요청한 유저와 글쓴이의 일치 여부 확인이 필요

    ​         => if request.user == review.user:

    ​		1 ) 로그인 된 상태 : request의 방식이 POST인지 아닌지에 따라 나눠 작업

    ​	    2 ) 로그인이 안 된 상태 : 리뷰 게시판으로 redirect

    ```python
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
    ```



    ** 삭제

      @ 삭제의 경우, detail 페이지에서 본 글의 작성자에게만 버튼이 보이도록 설계

    ```html
    {% if review.user == request.user %}
        <form action="{% url 'community:delete' review.pk %}" method='POST'>
            {% csrf_token %}
            <button>삭제</button>
        </form>
    {% endif %}
    ```



      @ POST 방식이기 때문에 @require_POST, @login_required 를 동시에 달아줌

    ```python
    @require_POST
    @login_required
    def delete(request, detail_pk):
        review = get_object_or_404(Review, pk = detail_pk)
        if request.user == review.user:
            review.delete()
        return redirect('community:review_list')
    ```



  - **댓글 작성 / 삭제**  =>  `다시 공부 필요`

    ```python
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
    ```

    - Comment 생성 시 주의사항

      ** <u>**Comment 모델은 Review의 기본키와 User의 기본키를 참조**</u>

      => 즉, form에서의 content 만을 저장해주면 필수 값 부족으로 form.save()가 안 된다.

      ​    **<< 최초 save 시 commit=False 로 지정해주는 이유 >>**

      => 추가적으로 comment.user와 comment.review 로 필수 요소 할당

      => 그 후 comment.save()   `default가 commit=True`

    - Comment 삭제 시 주의사항

      => POST 방식이므로 @require_POST 필요

      => ***detail_pk, comment_pk 가 필요***

      ​	ㄱ. comment_pk 는 comment를 확인, 삭제하는 데 필요

      ​	ㄴ. detail_pk 는 redirect를 할 때 필요



- django_pjt3

  - 네비게이션 바 (base.html)

    - 로그인 시

      로그아웃 버튼이 보임

    - 비로그인 시

      회원가입/로그인 버튼이 보임

       => base.html 에서 분기처리로 구현

    ```html
    {% if user.is_authenticated %}
        <button><a href="{% url 'accounts:logout' %}">로그아웃</a></button>
    {% else %}
        <button><a href="{% url 'accounts:signup' %}">회원가입</a></button>
        <button><a href="{% url 'accounts:login' %}">로그인</a></button>
    {% endif %}
    ```

    - 리뷰 게시판 페이지의 새 글 쓰기 버튼과 동일 버튼 추가
    - 리뷰 게시판으로 이동하는 버튼 추가



##### ** 과정 후 총평

기능 구현 상에 필요할 것 같은 순서대로 접근하려고 하니, 약간의 의견 차이가 생겼습니다.

큰 차이는 없어서 쭉쭉 구현해 나가다보니 이전에 구현했던 것들을 다시 손 봐야 하는 경우가 많이 발생했습니다.

ex)

그래서 저 개인적으로는 필요 기능부터 구현하는 것도 맞지만, `다른 기능과는 가장 연관 관계가 없는 기능부터 구현하는 것이 나중에 수정할 일을 줄일 수 있는 방법`이라 느꼈습니다.



<u>다음부터는 기능 구현 시 독립적으로 구현 가능한 부분부터,</u>

<u>순차적으로 구현해 나가야겠습니다.</u>