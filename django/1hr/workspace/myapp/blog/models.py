from django.conf import settings
from django.db import models
from django.utils.text import slugify


class category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    img_url = models.URLField(null=True)
    ceated_at=models.DateTimeField(auto_now_add=True)
    slug=models.SlugField(unique=True)
    Category=models.ForeignKey(category, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_posts",
    )
    is_published = models.BooleanField(default=False)
    
    def save(self,*args, **kwargs):
        base_slug = slugify(self.title)
        self.slug = base_slug
        counter = 1
        while Post.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f'{base_slug}-{counter}'
            counter += 1
        super().save(*args, **kwargs)
      

     
    def __str__(self):
        return self.title
    
class AboutUs(models.Model):
    content=models.TextField()
