from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class Team(models.Model):
    team_name = models.CharField(max_length=250)
    manager = models.CharField(max_length=250, blank=True)
    def __str__(self):
        return self.team_name

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    
    


