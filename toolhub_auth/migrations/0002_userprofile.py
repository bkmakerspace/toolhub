# Generated by Django 2.1.4 on 2019-01-18 21:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import markdownx.models


def create_profiles(apps, schema_editor):
    """
    Previous signup code saved passwords in plaintext, clear passwords, create profiles
    """
    User = apps.get_model('toolhub_auth', 'User')
    UserProfile = apps.get_model('toolhub_auth', 'UserProfile')
    for user in User.objects.filter(profile__isnull=True):
        UserProfile.objects.create(user=user)
        user.set_unusable_password()
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('toolhub_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('text', markdownx.models.MarkdownxField(blank=True, verbose_name='Profile Text')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.RunPython(create_profiles, migrations.RunPython.noop),
    ]