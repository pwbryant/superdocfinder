from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Search Documents',header_text)
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

        table = self.browser.find_element_by_id('id_results_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
                any(row.text == 'atrazine result' for row in rows)
                )

        #Page Title and search bar are still there. User wants to search
        #for all papers regarding Iowa, because Waterborne carries out 
        #a lot of research there. They enter 'Iowa' and hit enter
        self.fail('Finish the test')

        #The page updates again with the new results

        #The User sees a document they are interested in and so they
        #click on a result, whereupon the document is downloaded to their
        #local computer

if __name__ == '__main__':
    unittest.main(warnings='ignore')
