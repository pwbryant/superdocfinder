from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from docfinder.models import Document
import os

class NewVisitorTest(FunctionalTest):

    def test_can_enter_search_term_and_retrieve_results(self):

        #User wants to find all documents that Waterborne has
        #concernging a variety of topics. They got to the homepage
        #of Waterborne's docfinder site
        self.browser.get(self.server_url)
        self.browser.implicitly_wait(3)
        #She notice the tile 'Document Finder' and a search bar
        self.assertIn('Waterborne-env Docfinder',self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Document Search Tool',header_text)
        inputbox = self.browser.find_element_by_id('id_search_term')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter search term(s)'
                )

        #User accidentilly hits 'Enter' and searches with no search terms
        #and nothing happens

        inputbox = self.browser.find_element_by_id('id_search_term')
        inputbox.send_keys('')
        inputbox.send_keys(Keys.ENTER) 

        #User enters junkSearch, but there aren't any papers pertaining
        #to junkSearch, so a result of 'No Results' is returned
    
        inputbox = self.browser.find_element_by_id('id_search_term')
        inputbox.send_keys('junkSearch')
        inputbox.send_keys(Keys.ENTER) 
        self.check_for_row_in_results_table('No Documents Found')
         
        #she types in 'atrazine' and hits enter to get all docs regarding 
        #atrazine.
        inputbox = self.browser.find_element_by_id('id_search_term')
        inputbox.send_keys('atrazine')

        #User hits ENTER and  the page is updated with the returned results. 
        inputbox.send_keys(Keys.ENTER)
        self.assertRegex(self.browser.current_url,'/search/display_results/')
        self.check_for_row_in_results_table('Big Time Atrazine Study')

        #Page Title and search bar are still there. User wants to search
        #for all papers regarding Missouri, because Waterborne carries out 
        #a lot of research there. They enter 'Missouri' and hit enter
        inputbox = self.browser.find_element_by_id('id_search_term')
        inputbox.send_keys('Missouri')
        inputbox.send_keys(Keys.ENTER) 

        #The page updates again with the new results
        self.check_for_row_in_results_table('Pesticide Study')

        #The User would like all papers mentioning atrazine and/or missouri
        inputbox = self.browser.find_element_by_id('id_search_term')
        inputbox.send_keys('atrazine Missouri')
        inputbox.send_keys(Keys.ENTER) 
        self.check_for_row_in_results_table('Big Time Atrazine Study')
        self.check_for_row_in_results_table('Pesticide Study')

        #The User sees a document they are interested in and so they
        #click on a result, whereupon the document is downloaded to their
        #local computer
        doc = Document.objects.first()
        os.chdir(self.DOWNLOAD_DIR)
        try:
            os.remove('test.csv')
        except:
            pass
        self.browser.find_element_by_id("search_result_%s" % doc.doc_id).click()
        input()
        downloaded_file = open(self.DOWNLOAD_DIR + '/test.csv','r')



