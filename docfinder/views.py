from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home_page(request):
    return render(request,'home.html',
            {'search_term_text':request.POST.get('search_term_text',''),
            })
