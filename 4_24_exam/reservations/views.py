# 각 문제를 해결하기 위하여 필요한 import문은 이곳에 작성합니다.
from django.shortcuts import render, redirect
from .models import Reservation
from .forms import ReservationForm

# date를 기준으로 내림차순으로 정렬한 reservations를 전달
def index(request):
    reservations = Reservation.objects.order_by('-date')
    context = {
        'reservations': reservations,
    }
    return render(request, 'reservations/index.html', context)

# 기본적인 POST, GET 분기 처리
def create(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservations:index')
    else:
        form = ReservationForm()
    context = {
        'form': form,
    }
    return render(request, 'reservations/create.html', context)