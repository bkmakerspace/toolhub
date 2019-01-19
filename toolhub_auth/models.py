from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from markdownx.models import MarkdownxField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        # create user profile to be edited by user later.
        UserProfile.objects.create(user=user)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Toolhub custom user
    """

    username = None  # unset username field from AbstractUser
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("first_name", "last_name")

    objects = UserManager()

    def __str__(self):
        if self.get_full_name():
            return self.get_full_name()
        return self.email

    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})


class UserProfile(TimeStampedModel):
    """
    Custom user profile page details
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    text = MarkdownxField(_("Profile Text"), blank=True)

    def __str__(self):
        return f"{self.user} profile"

    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.user_id})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create the user profile when a user is created"""
    if created:
        UserProfile.objects.create(user=instance)
