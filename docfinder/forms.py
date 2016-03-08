from django import forms
from docfinder.models import Search

EMPTY_ITEM_ERROR = "You can't have an empty Search object"
class SearchForm(forms.models.ModelForm):

    class Meta:
        model = Search
        fields = ('search_terms',)
        widgets = {
            'search_terms': forms.fields.TextInput(attrs={
                'placeholder': 'Enter search term(s)',
                'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'search_terms': {'required':EMPTY_ITEM_ERROR}
        }
