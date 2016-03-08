from .base import FunctionalTest
from unittest import skip
import time


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # User goes to home page and accidentilly hits Enter with an empty search bar
        self.browser.get(self.server_url)
        self.get_search_input_box().send_keys('\n')
        time.sleep(1)
        #The home page refreshes, and there is an error message saying that a blank 
        #has been entered
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You didn't enter any search terms")

        #The User then enters 'atrazine' and they get results
        self.get_search_input_box().send_keys('atrazine\n')
        time.sleep(1)
        self.check_for_row_in_results_table('Big Time Atrazine Study')
        #The User again hits Enter with an empty search bar

        self.get_search_input_box().send_keys('\n')
        time.sleep(1) 
        #A similar error message is displayed
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You didn't enter any search terms")

