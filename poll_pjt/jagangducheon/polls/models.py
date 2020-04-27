from django.db import models

# Create your models here.

class Poll(models.Model):
    poll_subject = models.CharField(max_length=100)
    question_a = models.CharField(max_length=50)
    question_b = models.CharField(max_length=50)
    vote_a = models.IntegerField(default=0)
    vote_b = models.IntegerField(default=0)

class Comment(models.Model):
    GENIUS_CHOICES = [
        ('up', '위쪽'),
        ('down', '아래쪽'),
    ]
    choice = models.CharField(max_length=10, choices=GENIUS_CHOICES, blank=False, default='Unspecified')
    writer = models.CharField(max_length=100)
    content = models.TextField()
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)