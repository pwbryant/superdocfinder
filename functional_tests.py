from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()


    def tearDown(self):
        self.browser.quit()


    def check_for_row_in_results_table(self,row_text):
        table = self.browser.find_element_by_id('id_results_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])


    def test_can_enter_search_term_and_retrieve_results(self):
        #User wants to find all documents that Waterborne has
        #concernging a variety of topics. They got to the homepage
        #of Waterborne's docfinder site
        self.browser.get('http://localhost:8000')
        self.browser.implicitly_wait(3)
        #She notice the tile 'Document Finder' and a
        #a search bar
        self.assertIn('Waterborne-env Docfinder',self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Document Search Tool',header_text)
        inputbox = self.browser.find_element_by_id('id_search_term')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter search term(s)'
                )

        #she types in 'atrazine' and hits enter to get all docs regarding 
        #atrazine.
        inputbox.send_keys('atrazine')

        #User hits ENTER and  the page is updated with the returned results. 
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_results_table('Big Time Atrazine Study')

        self.fail('Finish the test')
        #Page Title and search bar are still there. User wants to search
        #for all papers regarding Iowa, because Waterborne carries out 
        #a lot of research there. They enter 'Iowa' and hit enter
        inputbox = self.browser.find_element_by_id('id_search_term')
        inputbox.send_keys('Iowa')
        inputbox.send_keys(Keys.ENTER) 

        #The page updates again with the new results
        self.check_for_row_in_results_table('Iowa result')

        #The User sees a document they are interested in and so they
        #click on a result, whereupon the document is downloaded to their
        #local computer


if __name__ == '__main__':
    unittest.main(warnings='ignore')
