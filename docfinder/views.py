from django.shortcuts import render
from django.http import HttpResponse
import pysolr

# Create your views here.
def home_page(request):
    if len(request.GET) > 0:
        search_terms = request.GET['search_term_text']
        solr = pysolr.Solr('http://localhost:8983/solr/testcore',timeout=10)
        results = solr.search(search_terms).__dict__['docs']

        if len(results) > 0:
            return render(request,'home.html',
                    {'search_results':results}
                    )
    
    return render(request,'home.html')
