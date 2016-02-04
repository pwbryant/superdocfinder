from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
import pysolr

from docfinder.views import home_page, search, get_search_results, download
from docfinder.models import Search

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
    
    def test_saving_and_retrieving_searches(self):
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
        response = self.client.get("/search/get_search_results/atrazine_missouri/")
        self.assertTemplateUsed(response, 'search.html')

    def test_get_search_url_resolves_to_get_search_results_view(self):

        found = resolve('/search/get_search_results/atrazine_missouri/')
        self.assertEqual(found.func, get_search_results)
 

class SearchTests(TestCase):
     
    def test_search_url_resolves_to_search_view(self):
        found = resolve('/search/new_search')
        self.assertEqual(found.func, search)
 

    def test_search_only_saves_items_when_necessary(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['search_term_text'] = ''
        search(request)
        self.assertEqual(Search.objects.count(), 0)
        

    def test_search_can_save_POST_requests(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['search_term_text'] = 'atrazine missouri'
        
        response = search(request)

        self.assertEqual(Search.objects.count(),1)
        newly_saved_search = Search.objects.first()
        self.assertEqual(newly_saved_search.search_terms, 'atrazine missouri')
   

    def test_search_redirects_correctly_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        search_terms = 'atrazine missouri'
        
        request.POST['search_term_text'] = search_terms
        
        search_terms_url ='atrazine_missouri'
        response = search(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'],'/search/get_search_results/%s/' % search_terms_url)

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

    def test_can_locate_downloaded_doc_from_download_view(self):
        
        response = download(HttpRequest,'1')
        print(response)
        print(response['Content-Disposition'])
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="test.csv"')

        















