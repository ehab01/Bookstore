from django.db import models
from django.contrib.auth.models import AbstractUser , Group, Permission
from django.db import IntegrityError
from django.core.validators import RegexValidator

phone_number_validator = RegexValidator(
    regex=r'^\d{11}$',
    message="Phone number must be exactly 11 digits."
)

class User(AbstractUser):
    first_name = models.CharField(max_length=30, unique=False, null=False)
    last_name = models.CharField(max_length=30, unique=False, null=False)
    contact_number = models.CharField(
        max_length=11,
        unique=True,
        null=False,
        validators=[phone_number_validator]
    )
    user_email = models.CharField(max_length=254, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    USERNAME_FIELD = "contact_number"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        self.username = self.contact_number
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.contact_number)

    class Meta:
        verbose_name_plural = "Users"