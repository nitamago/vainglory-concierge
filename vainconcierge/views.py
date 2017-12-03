from django.http.response import HttpResponse
from django.shortcuts import render

def index_page(request):
    return render(request, 'vainconcierge/index.html')
