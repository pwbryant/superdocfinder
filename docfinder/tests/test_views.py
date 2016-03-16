from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
import pysolr
import os
from datetime import datetime
from docfinder.views import home_page, search, get_search_results, display_results, download
from docfinder.models import Search, Document, Searches, Result
from django.utils.html import escape
from docfinder.forms import SearchForm, EMPTY_SEARCH_ERROR
from django.db import transaction
# Create your tests here.


class HomePageTest(TestCase):

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], SearchForm)


class SearchResultsTests(TestCase):

    def test_display_results_in_correct_order(self):

        #not sorted
        request = HttpRequest()
        response = display_results(request,'atrazine_missouri_1')
        self.assertIn('2013',str(response.content).split('Year:')[1])

        #sorted by year
        request = HttpRequest()
        response = display_results(request,'atrazine_missouri_2')
        self.assertIn('2016',str(response.content).split('Year:')[1])

    
    def test_get_search_results_renders_search_html_for_backend_error(self):
        Search.objects.create(search_terms='atrazine')
        response = self.client.get("/search/get_search_results/atrazine_1")
        self.assertTemplateUsed(response, 'search.html')


    def test_displays_search_form(self):
        response = self.client.get('/search/display_results/atrazine/')
        self.assertIsInstance(response.context['form'], SearchForm)
        self.assertContains(response, 'name="search_terms"')


    def test_uses_search_template(self):
        response = self.client.get("/search/display_results/atrazine_missouri/")
        self.assertTemplateUsed(response, 'search.html')


    def test_get_search_results_url_resolves_to_get_search_results_view(self):
        found = resolve('/search/get_search_results/atrazine_missouri/')
        self.assertEqual(found.func, get_search_results)


    def test_get_search_results_creates_results_objects(self):
        request = HttpRequest()
        search = Search(search_terms = 'atrazine missouri')
        search.save()
        searches = Searches(search_id = search,time=datetime.now())
        searches.save()
        document1 = Document(doc_id = '1', filename = 'test.csv', author="Paul Bryant", title = "Here is the atrazine title")
        document2 = Document(doc_id = '2', filename = 'test2.csv', author="Gill Humphry", title = "document 2 title")

        document1.save()
        document2.save()

        get_search_results(request,'atrazine_missouri_1')
    
        newly_saved_results = Result.objects.all()
        result1 = newly_saved_results[0]
        result2 = newly_saved_results[1]

        self.assertEqual(Result.objects.count(),2)
        self.assertEqual(result1.doc_id,document1)
        self.assertEqual(result2.doc_id,document2)


    def test_get_search_results_creates_Searches_objects(self):
        request = HttpRequest()
        search = Search(search_terms = 'atrazine missouri')
        search.save()
        get_search_results(request,'atrazine_missouri_1')
        newly_saved_Searches = Searches.objects.all()[0]
        self.assertEqual(Searches.objects.count(),1)
        self.assertEqual(newly_saved_Searches.search_id,search)


    def test_get_search_results_handles_empty_results(self):
        request = HttpRequest()
        Search.objects.create(search_terms = 'junkSearch')
        get_search_results(request,'junkSearch_1')
        self.assertEqual(Result.objects.count(),0)
        
 
    def test_get_search_results_veiw_redirects_correctly_after_being_called(self):
        request = HttpRequest()
        search = Search(search_terms = 'atrazine')
        search.save()
        Document.objects.create(doc_id='1')
        search_terms_url = 'atrazine_1'
        response = get_search_results(request,search_terms_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'],'/search/display_results/%s/' % search_terms_url)


class SearchTests(TestCase):
     
    def post_invalid_input(self):
        return self.client.post(
            '/search/new_search',
            data={'search_terms': '','choice_field':'1'}
        )
    

    def test_for_invalid_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Search.objects.count(), 0)


    def test_for_invalid_input_renders_home_template(self):
        response = self.post_invalid_input() 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], SearchForm)


    def test_validation_errors_are_shown_on_home_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_SEARCH_ERROR))


    def test_search_func_deals_with_duplicate_search_terms(self):
        Search.objects.create(search_terms = 'atrazine')
        request = HttpRequest()
        request.method = 'POST'
        request.POST['search_terms'] = 'atrazine'
        request.POST['choice_field'] = '1'
        response = search(request)
        self.assertEqual(Search.objects.count(),1)
        self.assertEqual(response.status_code, 302)


    def test_search_url_resolves_to_search_view(self):
        found = resolve('/search/new_search')
        self.assertEqual(found.func, search)
 

    def test_search_can_save_POST_and_create_Search_objects(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['search_terms'] = 'atrazine missouri'
        request.POST['choice_field'] = '1'
        
        response = search(request)

        self.assertEqual(Search.objects.count(),1)
        newly_saved_search = Search.objects.first()
        self.assertEqual(newly_saved_search.search_terms, 'atrazine missouri')


    def test_search_redirects_correctly_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        search_terms = 'atrazine missouri'
        
        request.POST['search_terms'] = search_terms
        request.POST['choice_field'] = '1'
        
        search_terms_url ='atrazine_missouri_1'
        response = search(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'],'/search/get_search_results/%s' % search_terms_url)


class DownloadResultsTest(TestCase):      

    def test_download_url_resolves_to_download_view(self):
        found = resolve('/search/download/1/')
        self.assertEqual(found.func, download)

    def test_download_view_locates_for_download_the_desired_document(self):
        
        document = Document.objects.create(doc_id = '1', filename = 'UT_test.csv')
        response = download(HttpRequest,'1')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="UT_test.csv"')
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        DOWNLOAD_DIR = os.path.abspath(os.path.join(BASE_DIR,'../docs'))
        os.chdir(DOWNLOAD_DIR) 
        doc = open('UT_test.csv','r').read()
        self.assertEqual(response.content.decode(),doc)
        















