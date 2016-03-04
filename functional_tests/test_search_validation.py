from .base import FunctionalTest
from unittest import skip



class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # User goes to home page and accidentilly hits Enter with an empty search bar

        #The home page refreshes, and there is an error message saying that a blank 
        #has been entered

        #The User then enters 'atrazine' and they get results

        #The User again hits Enter with an empty search bar

        #A similar error message is displayed
        self.fail("write me!")

