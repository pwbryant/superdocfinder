from django.db import models

# Create your models here.

class Search(models.Model):
    search_terms = models.TextField(default='')
    
