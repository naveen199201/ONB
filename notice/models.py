from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.utils import timezone


# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user_id, filename)

USER_CHOICES =(
    ("0", "student"),
    ("1", "admin"),
    ("2", "coadmin")
)

YEAR_CHOICES = (
    ('1','First'),
    ('2','Second')
)

SPECIALIZATION = (
    ('0','None'),
    ('1','Marketing'),
    ('2','Finance'),
    ('3','Systems'),
    ('4','HR'),
    ('5','Logistics and supply chain')
)

class User(AbstractUser):
    role = models.CharField(choices=USER_CHOICES, default='0', max_length=1)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    batch = models.CharField(choices = YEAR_CHOICES, default='1', max_length=2)
    specialization = models.CharField(choices= SPECIALIZATION, default='0', max_length=2)
    profile = models.ImageField(upload_to = user_directory_path)
    last_read = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.user.username

TYPE_CHOICES = (
        ("1", "Circulars"),
        ("2", "Results"),
        ("3", "Payments"),
        ("4", "Workshops"),
        ("5", "Remainders"),
        ("6", "New activity")
)

class Post(models.Model):
    post_type = models.CharField(
        max_length=2,
        choices = TYPE_CHOICES,
        default='1'
    )
    title = models.CharField(max_length=20)
    description = models.TextField()
    target_year = models.CharField(
        max_length=2,
        choices = YEAR_CHOICES,
        default='1'
    )
    draft = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='uploads/',blank=True,null=True)
    modified_at = models.DateTimeField(auto_now=True)
    target_audience = models.CharField(
        max_length=2,
        choices=SPECIALIZATION,
        default='0'
    )
    def __str__(self) -> str:
        return self.title