from django.shortcuts import render
from django.http import HttpResponse
import pysolr

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        search_terms = request.POST['search_term_text']
        solr = pysolr.Solr('http://localhost:8983/solr/testcore',timeout=10)
        results = solr.search(search_terms)
        results = results.__dict__
        title = results['docs'][0]['title']
        print(title)
        return render(request,'home.html',
                {'search_term_text':title,
                })

    else:
        return render(request,'home.html',
                {'search_term_text':request.POST.get('search_term_text',''),
                })
