# Generated by Django 3.1.6 on 2022-01-02 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gmailservice', '0004_auto_20220102_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mails',
            name='date',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]
