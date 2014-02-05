from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from math import exp
from datetime import datetime

class Category(models.Model):
    short_name = models.CharField(max_length=32)
    long_name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.short_name


class Feed(models.Model):
    zero_update_time = datetime.fromtimestamp(0, timezone.utc)
    category = models.ForeignKey(Category)
    url = models.URLField(max_length=256)
    img_url = models.URLField(max_length=256, blank=True)
    source_url = models.URLField(max_length=256, blank=True)
    fid = models.CharField(max_length=128, blank=True)
    title = models.CharField(max_length=128, blank=True)
    last_update_time = models.DateTimeField(default=zero_update_time)

    def __unicode__(self):
        return self.url


class Article(models.Model):
    feed = models.ForeignKey(Feed)
    url = models.URLField(max_length=256)
    pub_time = models.DateTimeField()
    aid = models.CharField(max_length=128)
    title = models.CharField(max_length=256)
    last_update_time = models.DateTimeField()
    content = models.TextField()
    summary = models.TextField()
    score = models.PositiveIntegerField()
    score_update_time = models.DateTimeField()
    voters = models.ManyToManyField(User)

    def hotness(self):
        # implements N(t) = N(0) * e ^ (-t/theta)
        # theta = 28800, time needed to reduce at 63%
        timedelta = timezone.now() - self.score_update_time
        timedelta = timedelta.total_seconds()
        hotness = self.score * exp(-timedelta / 28800)
        # hotness = score * exp(-timedelta / 3600)
        return hotness

    def __unicode__(self):
        return self.title
