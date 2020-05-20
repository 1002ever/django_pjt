## \# 구현 사항



\* **<u>*실제 코드 구현 순서*</u>**

   => 회원가입, 로그인, 로그아웃 구현

   => Movie, Genre 모델링 및 loaddata로 데이터 저장

   => superuser 생성, admin 사이트에 Movie, Genre 추가

   => 장고 paginator, 부트스트랩 pagination 적용

   => Movie 좋아요 구현 ( Movie 모델에 like_users 필드 추가 )

   => Movie 10개 Random 추천 구현



\* **<u>*앱 별 기능 및 상세 구현 과정*</u>**

- accounts

  - 회원가입

  - 로그인

  - 로그아웃



- movies

  - Movie, Genre 데이터 - 장고 loaddata 를 이용해 저장

    1. dummy를 생성하여 load

    2. json 같은 파일을 load

       => 해당 프로젝트에선 2번 방식 채택

       ㄱ. 적용할 Model이 있는 app 내부에 fixtures 라는 폴더 생성

       ㄴ. fixtures 폴더 내부에 json 파일 저장

       ㄷ. 터미널에서 `python loaddata [app이름]/fixtures/[파일명].[확장자]` 수행



  - 영화  나열 페이지(index 페이지 역할)

    => 장고 paginator 로 구현

    - 20개씩 묶어 한 페이지에 할당

    ```python
    # 적용 순서
    # 1. import
    from django.core.paginator import Paginator

    # 2. 모든 객체 불러오고
    # 3. Paginator로 일정 개수로 쪼개어 객체로 저장
    movies = Movie.objects.all()
    paginator = Paginator(movies, 20)

    # 4. request.GET 의 자료 중 'page' 값을 저장
    # 5. 해당 페이지의 movie 모음 객체를 따로 저장
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 6. context에 담아 html에 전달
    # 7, html에서 {% for movie in page_obj %} 로 해당 페이지의 movie 객체 호출 가능
    ```



    => 부트스트랩 pagination 으로 html 페이지 내에서 `페이지 네이게이터 부분` 구현

    ​	\<\< django_pjt5/movies/templates/movies/movie_list.html 다시 보고 공부 필요,,  \>\>



  - 영화 10개 추천 - 랜덤

    ㄱ.  Movie.objects.order_by("?")[:10]

    ​      로 랜덤 정렬 후 10개 querySet을 뽑기

    ㄴ. movies를 context로 묶어 해당 html로 전달하여 사용



  - 영화 좋아요 구현

    ㄱ. 로그인 되어있으면 보이는 하트(i 태그)를 html에 추가

    ㄴ. 하트가 담겨있는 i 태그를 JS 코드에서 querySelector로 잡기

    ㄷ. forEach 로 하트를 돌며 EventListener 달기

    ​	 => ***단, 저마다 다른 영화와 매칭되므로 addEventListener를 달 때 movie.id로 구분이 필요.***

    ​			a. html에서 for문을 돌며 movie 옆에 하트를 붙여줬으므로, movie 데이터에 접근이 가능

    ​				=> 태그의 data-set 속성을 이용하여 movid.id 값을 JS로 넘겨줌

                         ```html
     <i class="fas fa-heart fa-lg" style="color:crimson" data-id="{{ movie.id }}"></i>
                         ```

    ​			b. JS에서 event.target.dataset.id 로 movie.id 값을 얻을 수 있음

    ​		    c. movie.id 를 이용한 url 요청을 axios 함수의 인자로 넣음

    ​				=> Movie 모델의 like_users 필드를 조정하는 views.py의 like 함수로 연결

    ​						`DB변경 + Json 리턴(status, count 정보를 담은)`

    ​			d. 받은 Json 속 data를 통해 분기 처리하여 태그의 속성값 변경



##### ** 과정 후 총평

- bootstrap cdn으로 활용, 다음번엔 static으로 사용해볼 것 + Image 업로드도..

- paginator, pagination 는 게시판에서는 거의 필수적으로 사용될 것이므로 매번 다른 형태의 페이지 네비게이터를 만들어보자.
- 좋아요 AJAX로 구현하는 방법, 흐름과 코드가 아직 익숙치 않으니 반복 숙달 필요.