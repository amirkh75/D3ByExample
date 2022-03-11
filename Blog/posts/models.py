from django.db import models
from django.utils import timezone
from django.utils.translation import activate
from users.models import CustomUser
from django.urls import reverse
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()
    published = PublishedManager()

    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return f'{self.title}-{self.body[:50]}'

    def get_absolute_url(self):
        return reverse('posts:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.title)
            while Post.objects.filter(slug=self.slug).count() != 0:
                self.slug = self.slug + str(Post.objects.filter(slug=self.slug).count())

        return super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
