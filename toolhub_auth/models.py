from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from markdownx.models import MarkdownxField
from memoize import memoize, delete_memoized

from utils.templatetags.gravatar import gravatar_url


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

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        # Create the user profile when a user is created
        if created:
            UserProfile.objects.create(user=self)

    @memoize(timeout=2)
    def has_clearance(self, tool):
        return self.tool_permissions.filter(tool=tool).exists()

    def __del__(self):
        delete_memoized(self.has_clearance)

    def get_avatar_url(self, size):
        if not hasattr(self, "_social_account"):
            try:
                self._social_account = self.socialaccount_set.latest("id")
            except SocialAccount.DoesNotExist:
                self._social_account = None
        if self._social_account:
            img_urls = {
                k: v
                for k, v in self._social_account.extra_data.get("user", {}).items()
                if k.startswith("image_")
            }
            if img_urls:
                return self._select_image_url(size, img_urls)
        return gravatar_url(self.email, size)

    def _select_image_url(self, target_size, urls):
        sizes = sorted([int(u.split("_")[1]) for u in urls.keys()], reverse=True)
        selected_size = sizes[0]
        for size in sizes:
            if size < target_size:
                break
            selected_size = size
        return urls["image_{}".format(selected_size)]


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
