from django.shortcuts import redirect, render
from django.http import HttpResponse
import pysolr
from docfinder.models import Search, Document, Searches, Result
from docfinder.forms import SearchForm, EMPTY_SEARCH_ERROR
import os
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import IntegrityError
# Create your views here.

def home_page(request):
    return render(request, 'home.html', {'form': SearchForm(initial={
        'choice_field':'1'
        })
    })


def search(request):
    form = SearchForm(data=request.POST,initial={
        'choice_field':request.POST['choice_field']
        })
    if form.is_valid():
        search_terms = request.POST['search_terms'].lower().split()
        search_terms.sort()
        search_results_order = request.POST['choice_field']
        search_terms_url = '_'.join(search_terms + [search_results_order])
        search_terms_str = ' '.join(search_terms)
        try:
            search = Search(search_terms = search_terms_str)
            search.full_clean()
            search.save()
        except ValidationError:
            pass 
        return redirect('get_search_results',search_terms_url)
    
    else:
        return render(request, 'home.html',{'form':form})
    

def get_search_results(request,search_terms):
    results_ordering = search_terms[-1]
    search_terms_for_sql = search_terms[:-2].replace('_',' ')
    search_terms_for_solr = search_terms[:-2].replace('_','+')
    solr_search = 'title_sf:%s*^6 OR "%s"^3 OR partialSearch:%s^2 OR %s' % (search_terms_for_solr,search_terms_for_solr,search_terms_for_solr,search_terms_for_solr)
    solr = pysolr.Solr('http://localhost:8983/solr/testcore',timeout=10)
    results = solr.search(solr_search,**{'hl':'true','hl.fl':'doc_body_sf','hl.snippets':5,'hl.fragsize':10}).__dict__['docs']
    search = Search.objects.get(search_terms = search_terms_for_sql)
    searches = Searches.objects.create(search_id = search)
    if len(results) > 0:
        for solr_result in results:
            document_objects = Document.objects.filter(doc_id = solr_result['sid'][0])
            if len(document_objects) > 0:
                document = document_objects[0]
                Result.objects.create(doc_id = document, searches_id = searches)
            else:
                form = SearchForm(initial={'choice_field':results_ordering})
                admin_error = 'See Admin about search term(s) "%s"' % search_terms_for_sql
                return render(request,'search.html',
                        {'admin_error':admin_error,'search_terms':search_terms,'form':form})

    return redirect('display_results', search_terms)


def display_results(request, search_terms):
    results_ordering = search_terms[-1]
    search_terms_for_display = search_terms[:-2].replace('_',' ')
    search_terms_for_solr = search_terms[:-2].replace('_','+')
    solr_search = 'title_sf:%s*^6 OR "%s"^3 OR partialSearch:%s^2 OR %s' % (search_terms_for_solr,search_terms_for_solr,search_terms_for_solr,search_terms_for_solr)


    solr = pysolr.Solr('http://localhost:8983/solr/testcore',timeout=10)
    highlight_params = {'hl':'true','hl.fl':'doc_body_sf','hl.snippets':5,'hl.fragsize':40,'hl.simple.pre':'<b>','hl.simple.post':'</b>'}
    if results_ordering == '2':
        results = solr.search(solr_search,sort='year desc',**highlight_params).__dict__
    else:
        results = solr.search(solr_search,**highlight_params).__dict__
    for result in results['docs']:
        result['highlighting'] = ''
        for key in result.keys():
            if type(result[key]) == list:
                result[key] = result[key][0]
            result['highlighting'] = '<br>'.join(results['highlighting'][result['id']]['doc_body_sf'])
    return render(request,'search.html',
            {'search_results':results,'search_terms':search_terms_for_display,'form':SearchForm(initial={'choice_field':results_ordering})})


def download(request,doc_id):
    document = Document.objects.get(doc_id = doc_id)
    file_name = document.filename
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DOWNLOAD_DIR = os.path.abspath(os.path.join(BASE_DIR,'../docs'))
    os.chdir(DOWNLOAD_DIR)
    content = open('%s' % file_name,'rb')
    response = HttpResponse(content,content_type = 'application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s"' % file_name 
    return response
