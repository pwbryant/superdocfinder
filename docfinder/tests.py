from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
import pysolr

from docfinder.views import home_page
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
    
    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Search.objects.count(), 0)

    def test_home_page_can_save_POST_requests(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['search_term_text'] = 'atrazine missouri'
        
        response = home_page(request)

        self.assertEqual(Search.objects.count(),1)
        newly_saved_search = Search.objects.first()
        self.assertEqual(newly_saved_search.search_terms, 'atrazine missouri')
    
    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['search_term_text'] = 'atrazine missouri'
        
        response = home_page(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'],'/')


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


        

        


















