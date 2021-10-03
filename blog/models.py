from datetime import datetime

from django.db import models
from django.urls import reverse

from autoslug.fields import AutoSlugField


class BlogPostQueryset(models.QuerySet):

    def published(self):
        return self.filter(published=True)

    def draft(self):
        return self.filter(published=False)


class BlogPost(models.Model):
    STATUS = (
        (0, "Draft"),
        (1, "Publish")
    )

    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='blog')
    description = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    pub_date = models.DateTimeField(blank=True, null=True)

    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        verbose_name = ('blog post')
        verbose_name_plural = ('blog posts')
        ordering = ['pub_date']

    def save(self, *args, **kwargs):
        """
        Set publish date to the date when post's published status is switched to True, 
        reset the date if post is unpublished
        """
        if self.published and self.pub_date is None:
            self.pub_date = datetime.now()
        elif not self.published and self.pub_date is not None:
            self.pub_date = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    objects = BlogPostQueryset.as_manager()
