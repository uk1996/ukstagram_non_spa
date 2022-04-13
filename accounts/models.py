from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = 'MALE', '남' # DB 저장 text, 화면에 보여지는 text
        FEMALE = 'FEMALE', '여'

    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True, verbose_name='Introduction')
    phone_number = models.CharField(max_length=13, blank=True, validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")])
    gender = models.CharField(max_length=6, blank=True, choices=GenderChoices.choices)
    avatar = models.ImageField(blank=True, upload_to='accounts/avatar/%Y/%m/%d')