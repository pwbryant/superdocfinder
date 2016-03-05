from django.test import TestCase
from docfinder.models import Search, Document, Searches, Result

class ModelTest(TestCase):
    
    def test_saving_and_retrieving_search(self):
        first_search = Search()
        first_search.search_terms = 'atrazine'
        first_search.save()

        second_search = Search()
        second_search.search_terms = 'missouri'
        second_search.save()

        saved_searches = Search.objects.all()
        self.assertEqual(saved_searches.count(),2)

        first_saved_search = saved_searches[0] 
        second_saved_search = saved_searches[1]
        self.assertEqual(first_saved_search.search_terms, 'atrazine')
        self.assertEqual(second_saved_search.search_terms, 'missouri')
     

    def test_saving_and_retrieving_searches(self):
        search = Search(search_terms = 'atrazine')
        search.save()
        searches = Searches(search_id = search)
        searches.save()
        saved_searches = Searches.objects.all()
        saved_search = saved_searches[0]
        self.assertEqual(saved_searches.count(),1)
        self.assertEqual(saved_search.search_id.search_terms,search.search_terms)


    def test_saving_and_retrieving_documents(self):
        document = Document(doc_id = '1', filename='test.pdf', author="Slick Willy",abstract='here is an abstract')
        document.save()
        saved_document = Document.objects.first()
        self.assertEqual(saved_document.pk,document.pk)


    def test_saving_and_retrieving_results(self):
        search = Search(search_terms = 'atrazine')
        search.save()
        searches = Searches(search_id = search)
        searches.save()
        document = Document(doc_id = '1', filename='test.pdf', author="Slick Willy",abstract='here is an abstract')
        document.save()
        
        result = Result(doc_id = document, searches_id = searches)
        result.save()

        results = Result.objects.all()
        saved_result = results[0]

        self.assertEqual(results.count(),1)
        self.assertEqual(saved_result.pk,result.pk)
        self.assertEqual(saved_result.doc_id.pk, document.pk)
        self.assertEqual(saved_result.searches_id.pk,searches.pk)
        self.assertEqual(saved_result.searches_id.search_id.pk,search.pk)

