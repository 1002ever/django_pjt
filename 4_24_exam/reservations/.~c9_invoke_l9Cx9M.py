from django import forms
from .models import Reservation

# 기본적인 폼 구성
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'


