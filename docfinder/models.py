from django.db import models

# Create your models here.

class Search(models.Model):
    
    search_terms = models.TextField(unique=True)

    def __str__(self):
        return self.search_terms

class Searches(models.Model):

    search_id = models.ForeignKey(Search, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now = True)


class Document(models.Model):
    
    doc_id = models.IntegerField(unique=True)
    filename = models.TextField(unique=True)
    author = models.TextField()
    title = models.TextField(unique=True)


class Result(models.Model):

    doc_id = models.ForeignKey(Document)
    searches_id = models.ForeignKey(Searches)

