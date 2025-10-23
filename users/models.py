from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import Group


class Team(models.Model):
    team_name = models.CharField(max_length=250)
    manager = models.OneToOneField(
        "CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="manager_team",
    )

    def __str__(self):
        return self.team_name


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)
    team_id = models.ForeignKey(
        Team, on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="members"
    )
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE,
        null=True,
        blank=True)


    @property
    def is_trainer(self):
        """
        Convenience property used by templates/views to check if the user
        should be treated as a Trainer. Returns True if either:
        - the related StaffProfile has role == 'Trainer', or
        - the user belongs to a Group named 'Trainers' (fallback).

        This is a small, non-invasive helper so templates can use
        `user.is_trainer` instead of directly accessing profiles or groups.
        """
        try:
            if getattr(self, 'staffprofile', None) and self.staffprofile.role == 'Trainer':
                return True
        except Exception:
            pass
        # f
        try:
            return self.groups.filter(name__iexact='Trainers').exists()
        except Exception:
            return False
    
    @property
    def is_chef(self):
        try:
            if getattr(self, 'staffprofile', None) and self.staffprofile.role == 'Chef':
                return True
        except Exception:
            pass
        try:
            return self.groups.filter(name__icontains='chef').exists()
        except Exception:
            return False

    @property
    def is_doctor(self):
        try:
            if getattr(self, 'staffprofile', None) and self.staffprofile.role == 'Doctor':
                return True
        except Exception:
            pass
        try:
            return self.groups.filter(name__icontains='doctor').exists()
        except Exception:
            return False

    @property
    def is_dietician(self):
        try:
            if getattr(self, 'staffprofile', None) and self.staffprofile.role in ('Dietician', 'Dietitian'):
                return True
        except Exception:
            pass
        try:
            return self.groups.filter(name__icontains='diet').exists()
        except Exception:
            return False

    @property
    def is_manager(self):
        try:
            if getattr(self, 'staffprofile', None) and self.staffprofile.role == 'Manager':
                return True
        except Exception:
            pass
        try:
            return self.groups.filter(name__icontains='manager').exists()
        except Exception:
            return False

        
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    
    
  