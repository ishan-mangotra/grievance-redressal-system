# Generated by Django 2.0.2 on 2019-06-28 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190619_1632'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('can view dashboard', 'To open dashboard'), ('can view manager level', 'To open manager dashboard'), ('can view staff dashboard', 'To open staff dashboard'))},
        ),
    ]
