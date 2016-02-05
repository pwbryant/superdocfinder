from django.db import models

# Create your models here.

class Search(models.Model):
    search_terms = models.TextField(default='')

class Documents(models.Model):
    
    doc_id = models.TextField(default='',unique=True)
    filename = models.TextField(default='',unique=True)
    author = models.TextField(default= '')
    abstract = models.TextField(default='')
