from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLES = (
            (1, 'ProjectManager'),
            (2, 'collaborater'),
        )
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email = models.EmailField(('email address'), unique = True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    role = models.PositiveSmallIntegerField(choices=ROLES, blank=True, null=True)

    def __str__(self):
      return "{}".format(self.username)


