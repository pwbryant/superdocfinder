from django import forms

EMPTY_SEARCH_ERROR = "enter search terms"

class SearchForm(forms.Form):
    search_terms = forms.CharField(max_length=100,required=True,error_messages = {'required': EMPTY_SEARCH_ERROR},widget=forms.TextInput(attrs={'placeholder': 'Enter search term(s)',
                    'class': 'form-control input-lg',
                })
            )
    
 



    
        
