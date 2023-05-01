from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, auth

from tinymce.models import HTMLField 

# Create your models here.
category_options =(

    ('Entertainment', 'Entertainment'),
    ('Others', 'Others'),
    ('Politics', 'Politics'),
    ('Programming','Programming'),
    ('Sport', 'Sport'),
    ('Technology', 'Technology'),
    ('Others', 'Others'),
    
)

class Post(models.Model):
    Author = models.CharField(max_length = 100, default = 'admin')
    title = models.CharField(max_length = 100, null = False)
    category = models.CharField(max_length = 100, choices=category_options, default = 'Others')
    #body = models.CharField(max_length = 1000000, default = 'Blog main body')
    body = HTMLField()
    # likes = models.IntegerField(default=0)
    # dislikes = models.IntegerField(default=0)
    # hearts = models.IntegerField(default=0)
    references = models.CharField(max_length = 10000, null = True)
    time_created = models.DateTimeField(default = datetime.now, blank = True)

    def __str__(self):
        return self.title
    
