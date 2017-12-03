from django.http.response import HttpResponse

def index_page(request):
    return HttpResponse('This is urls test.')
