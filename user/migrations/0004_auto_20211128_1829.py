# Generated by Django 3.2.8 on 2021-11-28 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20211109_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('male', '男'), ('female', '女')], default='male', max_length=6, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gexing',
            field=models.CharField(blank=True, default='static/imgs/p8.jfif', max_length=100, verbose_name='个性签名'),
        ),
    ]
