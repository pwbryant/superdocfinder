from django.db import models

# Create your models here.

class Search(models.Model):
    search_terms = models.TextField(default='',unique=True)


class Searches(models.Model):
    search_id = models.ForeignKey(Search, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now = True)


class Documents(models.Model):
    
    doc_id = models.TextField(default='',unique=True)
    filename = models.TextField(default='',unique=True)
    author = models.TextField(default= '')
    abstract = models.TextField(default='')
