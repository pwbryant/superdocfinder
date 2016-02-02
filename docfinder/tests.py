from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
import pysolr

from docfinder.views import home_page


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
    

    def test_home_page_can_save__POST_requests_and_get_results(self):
        request = HttpRequest()
        request.method = 'POST'
        search_terms = 'atrazine Missouri'
        request.GET['search_term_text'] = search_terms
        
        response = home_page(request)


        

        


















