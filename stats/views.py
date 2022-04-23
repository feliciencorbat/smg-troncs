from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    return render(request, 'stats/home.html')


@login_required
def export(request):
    return render(request, 'stats/export.html')
