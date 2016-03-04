from .base import FunctionalTest
from unittest import skip



class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # User goes to home page and accidentilly hits Enter with an empty search bar
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_search_term').send_keys('\n')

        #The home page refreshes, and there is an error message saying that a blank 
        #has been entered
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You didn't enter any search terms")

        #The User then enters 'atrazine' and they get results
        self.browser.find_element_by_id('id_search_term').send_keys('atrazine')
        self.check_for_row_in_results_table('Big Time Atrazine Study')

        #The User again hits Enter with an empty search bar
        self.browser.find_element_by_id('id_search_term').send_keys('\n')

        #A similar error message is displayed
        self.check_for_row_in_results_table('Big Time Atrazine Study')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You didn't enter any search terms")

        self.fail("write me!")
