# Generated by Django 4.1.2 on 2023-01-08 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HelbManager', '0002_alter_project_resources'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectnotification',
            old_name='descriptoin',
            new_name='description',
        ),
        migrations.AddField(
            model_name='projectnotification',
            name='projectName',
            field=models.CharField(default='', max_length=200),
        ),
    ]
