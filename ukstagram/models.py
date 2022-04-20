from django.conf import settings
from django.db import models
from django.urls import reverse
import re


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 수정 시간

    class Meta:
        abstract = True

class Post(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='ukstagram/post/%Y/%m/%d')
    caption = models.TextField()
    tag_set = models.ManyToManyField('Tag', blank=True)
    location = models.CharField(max_length=100, blank=True)
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like_post_set')

    class Meta:
        ordering = ['-id']

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

    def is_like_user(self, user):
        return self.like_user_set.filter(pk=user.pk).exists()


class Comment(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name