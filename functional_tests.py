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

        #she types in 'atrazine' and hits enter to get all docs regarding 
        #atrazine. The page is updated with the returned results. 
        
        #Page Title and search bar are still there. User wants to search
        #for all papers regarding Iowa, because Waterborne carries out 
        #a lot of research there. They enter 'Iowa' and hit enter

        #The page updates again with the new results

        #The User sees a document they are interested in and so they
        #click on a result, whereupon the document is downloaded to their
        #local computer

if __name__ == '__main__':
    unittest.main(warnings='ignore')
