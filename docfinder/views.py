from django.shortcuts import redirect, render
from django.http import HttpResponse
import pysolr
from docfinder.models import Search

# Create your views here.

def home_page(request):
    return render(request, 'home.html')


def search(request):
    if len(request.POST['search_term_text'].split()) > 0:
        search_terms = request.POST['search_term_text'].lower().split()
        search_terms.sort()
        search_terms_url = '_'.join(search_terms)
        search_terms_str = ' '.join(search_terms)
        Search.objects.create(search_terms = search_terms_str)
        return redirect('/search/get_search_results/%s/' % search_terms_url)
    else:
        return redirect('/')
        

def get_search_results(request,search_terms):

    search_terms = ' '.join(search_terms.split('_'))
    solr = pysolr.Solr('http://localhost:8983/solr/testcore',timeout=10)
    results = solr.search(search_terms).__dict__['docs']
    return render(request,'search.html',
            {'search_results':results}
                    )

def download(request,doc_id):
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename="test.csv"'
    return response
