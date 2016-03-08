from .base import FunctionalTest
from selenium import webdriver


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        #User goes to homepage
        self.browser.get(self.server_url)
        self.browser.set_window_size(1028,768)
        
        #User notices the inputbox is nicely centered
        inputbox = self.get_search_input_box()
        self.assertAlmostEqual(
                inputbox.location['x'] + inputbox.size['width']/2,
                512,
                delta=5
                )


        #After searching for a document the User sees that the search/results' page input box is also centered
        inputbox.send_keys('atrazine missouri')
        inputbox = self.get_search_input_box()
        self.assertAlmostEqual(
                inputbox.location['x'] + inputbox.size['width']/2,
                512,
                delta=5
                )


