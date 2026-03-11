from django.db import models
from django.urls import reverse


class BlogPost(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True, help_text='Short summary for listing')
    cover_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})
