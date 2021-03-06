# Generated by Django 2.1.1 on 2018-10-11 03:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0003_auto_20181005_0355'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertool',
            name='state',
            field=models.CharField(choices=[('none', 'None'), ('unused', 'Unused'), ('loaned', 'Loaned'), ('disabled', 'Decommissioned')], default='none', editable=False, max_length=10),
        ),
        migrations.AlterField(
            model_name='toolhistory',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tool_history', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usertool',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
    ]
