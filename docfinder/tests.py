from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
import pysolr
import os
from datetime import datetime

from docfinder.views import home_page, search, get_search_results, download
from docfinder.models import Search, Document, Searches, Result

# Create your tests here.

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(),expected_html)
      

class SeachesModelTest(TestCase):
    
    def test_saving_and_retrieving_search(self):
        first_search = Search()
        first_search.search_terms = 'atrazine'
        first_search.save()

        second_search = Search()
        second_search.search_terms = 'missouri'
        second_search.save()

        saved_searches = Search.objects.all()
        self.assertEqual(saved_searches.count(),2)

        first_saved_search = saved_searches[0] 
        second_saved_search = saved_searches[1]
        self.assertEqual(first_saved_search.search_terms, 'atrazine')
        self.assertEqual(second_saved_search.search_terms, 'missouri')
        

class SearchResultsTests(TestCase):
    
    def test_uses_search_template(self):
        response = self.client.get("/search/display_results/atrazine_missouri/")
        self.assertTemplateUsed(response, 'search.html')


    def test_get_search_url_resolves_to_get_search_results_view(self):

        found = resolve('/search/get_search_results/atrazine_missouri/')
        self.assertEqual(found.func, get_search_results)

    def test_get_search_results_creates_results_objects(self):

        request = HttpRequest()
        search = Search(search_terms = 'atrazine missouri')
        search.save()
        searches = Searches(search_id = search,time=datetime.now())
        searches.save()
        document1 = Document(doc_id = '1', filename = 'test.csv', author="Paul Bryant", abstract = "Here is the atrazine abstract")
        document2 = Document(doc_id = '2', filename = 'test2.csv', author="Gill Humphry", abstract = "We studied stuff")

        document1.save()
        document2.save()

        get_search_results(request,'atrazine_missouri')
    
        newly_saved_results = Result.objects.all()
        result1 = newly_saved_results[0]
        result2 = newly_saved_results[1]

        self.assertEqual(Result.objects.count(),2)
        self.assertEqual(result1.searches_id, searches)
        self.assertEqual(result2.searches_id, searches)
        self.assertEqual(result1.doc_id,document1)
        self.assertEqual(result2.doc_id,document2)
        
 
    def test_get_search_veiw_redirects_correctly_after_being_called(self):
        request = HttpRequest()
        search = Search(search_terms = 'atrazine missouri')
        search.save()
        searches = Searches(search_id = search,time=datetime.now())
        searches.save()
        document1 = Document(doc_id = '1', filename = 'test.csv', author="Paul Bryant", abstract = "Here is the atrazine abstract")
        document2 = Document(doc_id = '2', filename = 'test2.csv', author="Gill Humphry", abstract = "We studied stuff")

        document1.save()
        document2.save()

        search_terms_url = 'atrazine_missouri'
        response = get_search_results(request,search_terms_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'],'/search/display_results/%s/' % search_terms_url)


   


class SearchTests(TestCase):
     
    def test_search_url_resolves_to_search_view(self):
        found = resolve('/search/new_search')
        self.assertEqual(found.func, search)
 

    def test_search_does_not_save_search_and_searches_objects_if_unneccesary(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['search_term_text'] = ''
        search(request)
        self.assertEqual(Search.objects.count(), 0)
        self.assertEqual(Searches.objects.count(),0)

        Search.objects.create(search_terms = 'atrazine missouri')
        request.POST['search_term_text'] = 'atrazine missouri'
        search(request)
        self.assertEqual(Search.objects.count(),1)
        


    def test_search_can_save_POST_and_create_Search_and_Searches_objects(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['search_term_text'] = 'atrazine missouri'
        
        response = search(request)

        self.assertEqual(Search.objects.count(),1)
        self.assertEqual(Searches.objects.count(),1)
        newly_saved_search = Search.objects.first()
        newly_saved_searches = Searches.objects.first()
        self.assertEqual(newly_saved_search.search_terms, 'atrazine missouri')
        self.assertEqual(newly_saved_searches.search_id.pk,newly_saved_search.pk)
        self.assertEqual(type(datetime.now()),type(newly_saved_searches.time))


    def test_search_redirects_correctly_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        search_terms = 'atrazine missouri'
        
        request.POST['search_term_text'] = search_terms
        
        search_terms_url ='atrazine_missouri'
        response = search(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'],'/search/get_search_results/%s' % search_terms_url)

        request = HttpRequest()
        request.method = 'POST'
        request.POST['search_term_text'] = ''

        response = search(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'],'/')




class DownloadResultsTest(TestCase):      

    def test_download_url_resolves_to_download_view(self):
        found = resolve('/search/download/1/')
        self.assertEqual(found.func, download)

    def test_download_view_locates_for_download_the_desired_document(self):
        
        document = Document.objects.create(doc_id = '1', filename = 'UT_test.csv')
        response = download(HttpRequest,'1')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="UT_test.csv"')
        os.chdir('/home/paul/MyCode/Django/test_docs') 
        doc = open('UT_test.csv','r').read()
        self.assertEqual(response.content.decode(),doc)
        















