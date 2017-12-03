from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponse
from django.utils.html import mark_safe
from .models import Data, Hero

def index_page(request):
    return render(request, 'vainpick/index.html', {
                  'Heros': Hero.objects.all,
                  })
