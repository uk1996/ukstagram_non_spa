from django.conf import settings
from django.db import models
from django.urls import reverse
import re


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='ukstagram/post/%Y/%m/%d')
    caption = models.TextField()
    tag_set = models.ManyToManyField('Tag', blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.caption


    def get_absolute_url(self):
        return reverse('ukstagram:post_detail', kwargs={'pk':self.pk})

    def extract_tag_list(self):
        tag_list = []
        for tag_name in re.findall(r'# ?([a-zA-Z\dㄱ-힣]+)', self.caption):
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list

    def remove_tag_in_caption(self):
        return re.sub(r'# ?[a-zA-Z\dㄱ-힣]+', '', self.caption).strip()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name