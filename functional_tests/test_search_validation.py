from .base import FunctionalTest
from unittest import skip
import time
from docfinder.forms import EMPTY_SEARCH_ERROR

class SearchValidationTest(FunctionalTest):

    
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_users_search_returns_results_not_attached_to_docs(self):
        # User searches for 'atrazine' and though this get results on 
        # the bacend, the results have been incorretly tited to a document 
        # in the database and thus the User recieves a message urging the 
        # User to contact the Admin.
        
        self.browser.get(self.server_url)
        self.get_search_input_box().send_keys('watershed\n')
        table = self.browser.find_element_by_id('id_results_div')
        error = table.find_element_by_tag_name('h1')
        self.assertEqual(error.text,'See Admin about search term(s) "watershed"')


    def test_error_messages_are_cleared_on_input(self):
        # User enters empty search, and gets and error
        self.browser.get(self.server_url)
        self.get_search_input_box().send_keys('\n')
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())

        # User starts typing in the input box to clear the error
        self.get_search_input_box().send_keys('a')

        # User is pleased to see that the error message disappears
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())


    def test_cannot_add_empty_list_items(self):
        # User goes to home page and accidentilly hits Enter with an empty search bar
        self.browser.get(self.server_url)
        self.get_search_input_box().send_keys('\n')
        time.sleep(1)
        #The home page refreshes, and there is an error message saying that a blank 
        #has been entered
        error = self.get_error_element()
        self.assertEqual(error.text, EMPTY_SEARCH_ERROR)

        #The User then enters 'atrazine' and they get results
        self.get_search_input_box().send_keys('atrazine\n')
        time.sleep(1)
        self.check_for_row_in_results_table('Big Time Atrazine Study')
        #The User again hits Enter with an empty search bar

        self.get_search_input_box().send_keys('\n')
        time.sleep(1) 
        #A similar error message is displayed
        error = self.get_error_element()
        self.assertEqual(error.text, EMPTY_SEARCH_ERROR)



