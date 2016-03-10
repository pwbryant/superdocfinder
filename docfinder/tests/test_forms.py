from django.test import TestCase
from docfinder.forms import SearchForm, EMPTY_SEARCH_ERROR


class SearchFormTest(TestCase):

    def test_form_search_input_has_placeholder_and_css_classes(self):
        form = SearchForm()
        self.assertIn('placeholder="Enter search term(s)"',form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())


    def test_form_validation_for_blank_items(self):
        form = SearchForm(data={'search_terms':''})
        self.assertFalse(form.is_valid())


