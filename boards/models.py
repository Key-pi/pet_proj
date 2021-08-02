import math

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe
from django.utils.text import Truncator
from simple_history.models import HistoricalRecords


from markdown import markdown


#
# class Photo(models.Model):
#     file = models.ImageField(upload_to='avatars/')
#     description = models.CharField(max_length=255, blank=True)
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         verbose_name = 'photo'
#         verbose_name_plural = 'photos'

#
# class User(AbstractUser):
#     photo = models.ForeignKey(Photo, blank=True, null=True, on_delete=models.SET_NULL)


class Categories(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Reader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reader_user', editable=False)
    adult = models.BooleanField(default=False)
    interests = models.ManyToManyField(Categories, related_name='interests', blank=True, null=True)
    is_super_user = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return self.user.username


class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='blogger_user', editable=False)
    birthday = models.DateField(default=timezone.now)
    country = models.CharField('Country', max_length=100, null=False, blank=False)
    city = models.CharField('City', max_length=100, null=False, blank=False)
    categories = models.ManyToManyField(Categories, related_name='categories_set', blank=True, null=True, )
    is_super_user = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return self.user.username


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    def get_post_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()

    class Meta:
        ordering = ['-pk', ]


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_update = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject

    def get_page_count(self):
        count = self.posts.count()
        pages = count / 20
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    update_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))


class GalleryImages(models.Model):
    image = models.ImageField(upload_to='gallery_topics')
    topic = models.ForeignKey(Topic, related_name='gallery_images', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
