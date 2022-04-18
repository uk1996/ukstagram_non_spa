from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = 'MALE', '남' # DB 저장 text, 화면에 보여지는 text
        FEMALE = 'FEMALE', '여'

    following_set = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='follower_set')

    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True, verbose_name='Introduction')
    phone_number = models.CharField(max_length=13, blank=True, validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")])
    gender = models.CharField(max_length=6, blank=True, choices=GenderChoices.choices)
    avatar = models.ImageField(blank=True, upload_to='accounts/avatar/%Y/%m/%d')

    @property # method를 field인것 처럼 사용
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return reverse('pydenticon_image', kwargs={'data':self.username})