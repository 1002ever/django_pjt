from django.db import models

# Create your models here.
class Reservation(models.Model):
    date = models.DateField()
    personnel = models.IntegerField()
    location = models.CharField(max_length=20)

# 외래기 적용, CASCADE 옵션 적용.
class Reply(models.Model):
    comment = models.TextField()
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)