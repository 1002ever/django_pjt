## django_pjt2



#### ** *필수 과제*

- Model 정의
- Form 정의
- Admin 설정
- variable routing  ==>  이제서야 익숙..
- DB에서 레코드 삭제 시 @require_POST 적용

- ***<u>create / update 함수는 구분 작성</u>,***

    ***create/update 함수는 <u>form.html 공유가 가능</u> 하다는 점을 숙지할 것***



ㄱ.  Model 정의 후 이를 Form으로 넘겨주기.

​      -> forms.py 참조.

​          폼 클래스 내부 class Meta 정의.

​          meta 내부에서 model과 field 할당



ㄴ. Admin

​     -> 설정할 때 마다 가물가물..

​         admin.py 참조. => 각 app 마다 있다.

```python
from django.contrib import admin
from .models import Review

# Register your models here.
admin.site.register(Review)
```



 ㄷ. @require_POST 적용

​	1. views.py에

​         from django.views.decorators.http import require_POST



   2. delete 함수

      ```python
      @require_POST
      def delete(request, pk):
          review = get_object_or_404(Review, pk=pk)
          review.delete()
          return redirect('community:review_list')
      ```



3. 삭제 버튼이 있는 html 문서

   ```http
   <form action="{% url 'community:delete' review.pk %}" method="POST">
     {% csrf_token %}
     <button class="btn btn-light font-weight-light">삭제</button>
   </form>
   ```

