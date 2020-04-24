# 4월 24일 월말평가



##### * 구현 내역

- signup, login, logout
- 게시글 작성
- 댓글 model migrate



** 전체적으로 난이도 평이 => 아래 html 문서 내부에서의 문법 봐두기

- 값을 이용한 분기, date 표기

```html
<h1>Reservation</h1>

<a href="{% url 'reservations:create' %}">create</a>
<hr>
<!-- personnel 값에 따른 분기, date 표기 명세대로 적용 -->
{% for reservation in reservations %}
    {% if reservation.personnel > 5 %}
        <p>{{ reservation.date | date:'Y년 m월 d일' }}</p>
        <p>{{ reservation.personnel }}</p>
        <p>{{ reservation.location }}</p>
    {% else %}
        <ul>
            <li>{{ reservation.date | date:'Y년 m월 d일' }}</li>
            <li>{{ reservation.personnel }}</li>
            <li>{{ reservation.location }}</li>
        </ul>
    {% endif %}
    <hr>
{% endfor %}
```

- 로그인 여부에 따른 분기 처리

```html
<h1>accounts</h1>

<!-- user 인증이 되었는지를 확인 후 분기 처리 -->
{% if user.is_authenticated %}
    <h3>{{ user.username }}</h3>
    <a href="{% url 'accounts:logout' %}">logout</a>
{% else %}
    <a href="{% url 'accounts:signup' %}">signup</a>
    <a href="{% url 'accounts:login' %}">login</a>
{% endif %}
```

- url name에 따른 분기 처리

```html
<!-- url_name에 따른 분기 처리 -->
{% if request.resolver_match.url_name == 'signup' %}
    <h1>signup</h1>
{% else %}
    <h1>login</h1>
{% endif %}

<form action="" method="POST">
    {% csrf_token %}
    {{ form }}
    <input type="submit">
</form>
```



- 전체적으로 django_pjt3 의 완벽한 하위 프로젝트