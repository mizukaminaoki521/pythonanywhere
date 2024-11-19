from django.db import models

class Post(models.Model):
    name = models.CharField('phrase', max_length=1000)
    micropost = models.CharField('tweet', max_length=2000, blank=True)

    def __str__(self):
        return self.name