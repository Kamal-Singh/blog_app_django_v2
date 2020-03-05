from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    image = models.URLField()
    content = models.TextField()
    date_created = models.DateTimeField('Date Created',auto_now_add=True)
    last_modified = models.DateTimeField('Last Modified',auto_now=True)
    slug = models.SlugField(max_length=200)
    author = models.ForeignKey(User, on_delete= models.CASCADE)

    class Meta():
        ordering: ['-date_created']
    
    def __str__(self):
        return self.title