from django.shortcuts import redirect, render
from django.http import HttpResponse
import pysolr
from docfinder.models import Search

# Create your views here.

def home_page(request):
    if request.method == 'POST':
        Search.objects.create(search_terms = request.POST['search_term_text'])
        return redirect('/')

    return render(request, 'home.html')


def search(request):
    if len(request.POST['search_term_text'].split()) > 0:
        search_terms = request.POST['search_term_text'].lower().split()
        search_terms.sort()
        search_terms = '_'.join(search_terms)
        Search.objects.create(search_terms = search_terms)
        return redirect('/search/%s/' % search_terms)
    else:
        return redirect('/')
        

def get_search_results(request,search_terms):

    search_terms = ' '.join(search_terms.split('_'))
    solr = pysolr.Solr('http://localhost:8983/solr/testcore',timeout=10)
    results = solr.search(search_terms).__dict__['docs']
    return render(request,'search.html',
            {'search_results':results}
                    )

    
def undefined(request):

    if request.GET.get('search_term_text') != None and len(request.GET['search_term_text'].split()) > 0:
        search_terms = request.GET['search_term_text']
        solr = pysolr.Solr('http://localhost:8983/solr/testcore',timeout=10)
        results = solr.search(search_terms).__dict__['docs']

        if len(results) > 0:
            return render(request,'home.html',
                    {'search_results':results}
                    )
        else:
            return render(request,'home.html',
                    {'search_results':[{'title':['No Documents Found']}]}
                    )

    
    return render(request,'home.html')
