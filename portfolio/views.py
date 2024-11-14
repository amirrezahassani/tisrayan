from django.shortcuts import render
from .models import PF
from django.shortcuts import get_object_or_404, get_list_or_404


def portfolio_view(request):
    portfolio = get_list_or_404(PF)
    return render(request, 'portfolio.html', {'portfolio': portfolio})


def portfolio_single(request, slug):
    portfolio = get_object_or_404(PF, slug=slug)
    return render(request, 'portfolio-single.html', {'portfolio': portfolio})
