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
    Author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 100, null = False)
    category = models.CharField(max_length = 100, choices=category_options, default = 'Others')
    body = HTMLField()
    likes = models.IntegerField(default = 0 )
    dislikes = models.IntegerField(default = 0 )
    references = models.CharField(max_length = 10000, null = True)
    time_created = models.DateTimeField(default = datetime.now, blank = True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    

    def __str__(self):
        return self.title
    

class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ': ' + str(self.post) + ': ' + str(self.value)
        
    class Meta:
      unique_together = ('user', 'post', 'value')

