# Generated by Django 3.1 on 2020-09-20 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellerCenter', '0010_auto_20200920_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referal',
            name='link',
            field=models.CharField(db_column='LINK', max_length=255, null=True),
        ),
    ]
