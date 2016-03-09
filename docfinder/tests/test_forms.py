from django.test import TestCase
from docfinder.forms import SearchForm, EMPTY_SEARCH_ERROR


class ItemFormTest(TestCase):

    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = SearchForm()
        self.assertIn('placeholder="Enter search term(s)"',form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())


    def test_form_validation_for_blank_items(self):
        form = SearchForm(data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['search_terms'],
            [EMPTY_SEARCH_ERROR]
        )
