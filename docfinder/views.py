from django.shortcuts import redirect, render
from django.http import HttpResponse
import pysolr
from docfinder.models import Search, Document, Searches, Result
from docfinder.forms import SearchForm
import os
from datetime import datetime
from django.core.exceptions import ValidationError
# Create your views here.

def home_page(request):
    return render(request, 'home.html', {'form': SearchForm()})


def search(request):
    search_terms = request.POST['search_terms'].lower().split()
    search_terms.sort()
    search_terms_url = '_'.join(search_terms)
    search_terms_str = ' '.join(search_terms)
    try:
        search = Search.objects.get(search_terms = search_terms_str)
    except Search.DoesNotExist:
        search = Search(search_terms = search_terms_str)
        try:
            search.full_clean()
            search.save()
        except ValidationError:
            error = "You didn't enter any search terms"
            return render(request, 'home.html',{"error":error,'form':SearchForm()})
        
    Searches.objects.create(search_id = search)
    return redirect('get_search_results',search_terms_url)
    

def get_search_results(request,search_terms):
    search_terms_for_solr = ' '.join(search_terms.split('_'))
    solr = pysolr.Solr('http://localhost:8983/solr/testcore',timeout=10)
    results = solr.search(search_terms_for_solr).__dict__['docs']
    searches = Searches.objects.last()
    for solr_result in results:
        document_objects = Document.objects.filter(doc_id = solr_result['id'])
        if len(document_objects) > 0:
            document = document_objects[0]
            Result.objects.create(doc_id = document, searches_id = searches)
    return redirect('display_results', search_terms)


def display_results(request, search_terms):
    search_terms = ' '.join(search_terms.split('_'))
    solr = pysolr.Solr('http://localhost:8983/solr/testcore',timeout=10)
    results = solr.search(search_terms,sort='year desc',rows=200).__dict__['docs']
    for result in results:
        for key in result.keys():
            if type(result[key]) == list:
                result[key] = ', '.join(result[key])

    return render(request,'search.html',
            {'search_results':results,'search_terms':search_terms,'form':SearchForm()}
                    )


def download(request,doc_id):
    document = Document.objects.get(doc_id = doc_id)
    file_name = document.filename
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DOWNLOAD_DIR = os.path.abspath(os.path.join(BASE_DIR,'../docs'))
    os.chdir(DOWNLOAD_DIR)
    content = open('%s' % file_name,'r')
    response = HttpResponse(content,content_type = 'application/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % file_name 
    return response
