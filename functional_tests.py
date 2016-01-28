from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_enter_search_term_and_retrieve_results(self):
        #User wants to find all documents that Waterborne has
        #concernging a variety of topics. They got to the homepage
        #of Waterborne's docfinder site
        self.browser.get('http://localhost:8000')
        self.browser.implicitly_wait(3)
        #She notice the tile 'Document Finder' and a
        #a search bar
        self.assertIn('Search Documents',self.browser.title)
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
