from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required()
def homeview(request):
    return render(request, 'dashboard.html')
