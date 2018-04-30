#-*- coding:utf-8 -*-

from django.shortcuts import render
from .models import Article

# Create your views here.
from django.http.response import HttpResponse
from django.utils.html import mark_safe
from django.db.models import Q

def top_page(request,seq=""):
    all = Article.objects.all().filter(Q(is_public=True))
    return render(request, 'blog/top.html', {"all": all})


def about_page(request):
    return render(request, 'blog/about.html', {})


def article_page(request, index=-1):
    if int(index) < 0:
        return HttpResponse("No such article")
    else:
        data = Article.objects.get(Q(id=index))
        return render(request, 'blog/article.html',
            {"data": data})
