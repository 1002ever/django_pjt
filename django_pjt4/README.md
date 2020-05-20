## \# 구현 사항



\* **<u>*실제 코드 구현 순서*</u>**

   => 회원가입, 로그인 구현

   => follow 구현을 위해 User를 커스터마이징

   => 영화 선택 페이지(dummy) url / view / html 설정 ( 회원가입하면 로그인 상태로 진입하게끔 )

   => Movie, Review 테이블 생성 ( Movie : Review = 1 : many )

   => 리뷰 수정, 리뷰 삭제 구현

   => 리뷰 '좋아요' 구현

   => 로그아웃 구현(네비게이션 바 부분 완성 - `로그인/로그아웃 상태에 따라 다르게 보이게끔`)

   => 댓글 작성 / 삭제 구현

   => User 상세 페이지, follow 구현



***<u>\* 모델링</u>***

User - Movie ( 1: many )

User - Review ( 1: many )  =>  글쓴이

User - Review ( many : many ) => 좋아요

Movie - Review ( 1: many)

Review - Comment ( 1:many )

User - User ( many : many ) => 팔로우



\* **<u>*앱 별 기능 및 상세 구현 과정*</u>**

- accounts

  - 회원가입

  - 로그인

  - 로그아웃

  - 유저 상세 페이지 -> 여기서 follow를 할 수 있음

    - 장고 내 User 모델을 커스터마이징

      \*\*\* ***settings.py에 AUTH_USER_MODEL 변수 값을 '앱.클래스명' 으로 지정하여***

      ​        ***기존의 값을 덮어 씌워줘야 적절히 이용 가능***

      ​        ex) get_user_model를 이용한 User 모델 호출(그래야 경로를 잘 찾음)



- articles

  - 영화 선택 페이지(index 페이지 역할)

    - Admin 권한자만 접근 가능한 Movie 테이블의 Title을 나열하는 페이지

      => 선택하면 해당 영화의 리뷰 게시판으로 이동 가능



  - 리뷰 게시판

    - 해당 리뷰 게시판에 접속하면 '리뷰 쓰기'라는 메뉴가 있음

      => 리뷰 게시판에 들어갔다는 것은 어느 영화를 선택했다는 말이므로

      ​     리뷰 작성 시 Review의 외래키인 movie 값을 자동으로 할당해주게끔 설계.

      => 기존엔 리뷰 작성 시 movie 값을 선택하게끔 해줬으나 Movie 테이블의 필드가 많아지면

      ​      이는 부적절한 방법이라 판단.

      > Tip.
      >
      > 모델 정의 시 또는 폼 정의 시
      >
      > \_\_str\_\_ 메서드를 오버라이딩하여 Object 정보가 아닌 개발자 원하는대로 표시할 수 있다.
      >
      > - 참조
      >
      > [https://sodocumentation.net/ko/django/topic/888/%EB%AA%A8%EB%8D%B8](https://sodocumentation.net/ko/django/topic/888/모델)

  - 리뷰 detail 페이지 - 좋아요 구현





##### ** 과정 후 총평

- 아직 bootstrap , image 업로드까지 다뤄보지 못한 점이 아쉽습니다.

  => 사이드 프로젝트로 5월 내로 꼭 다뤄보려고 합니다.

- User - Review ( many : many ) 로 설정 시  이름 충돌이 나기 떄문에 related_name을 사용한다는 점은

  이해가 됐지만, 그 충돌 과정이 명확하게 이해되지 않아서 더 공부가 필요할 것 같습니다.

- User - User ( many : many ) 의 경우는 더욱 더 불명확해서 구현 시 마다 이해해보려고 노력 중입니다.