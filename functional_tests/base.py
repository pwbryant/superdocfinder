from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from docfinder.models import Document
import os
import sys


class FunctionalTest(StaticLiveServerTestCase):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
    DOWNLOAD_DIR = os.path.abspath(os.path.join(BASE_DIR, 'Downloads'))
    
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        Document.objects.create(doc_id='1', filename = 'test.csv', author = "Paul Bryant", title = "Here is the Atrazine title")
        Document.objects.create(doc_id='2', filename = 'test2.csv', author = "Gary Smith", title = "title - We did a pesticide study in Missouri")
        
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.manager.showWhenStarting',False)
        profile.set_preference('browser.download.dir',self.DOWNLOAD_DIR)
        self.browser = webdriver.Firefox(profile)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_results_table(self, row_text):
        table = self.browser.find_element_by_id('id_results_div')
        rows = table.find_elements_by_tag_name('p')
        self.assertIn(row_text, [row.text for row in rows])

    def get_search_input_box(self):
        return self.browser.find_element_by_id('id_search_terms')


