# Generated by Django 3.1.3 on 2021-07-26 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inputForm', '0012_auto_20210713_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soiltempmodel',
            name='jam',
            field=models.CharField(choices=[('06:00', '06:00'), ('03:00', '03:00'), ('12:00', '12:00'), ('00:00', '00:00'), ('09:00', '09:00')], default='00:00', max_length=10),
        ),
        migrations.AlterField(
            model_name='soiltempmodelcilacap',
            name='jam',
            field=models.CharField(choices=[('06:00', '06:00'), ('03:00', '03:00'), ('12:00', '12:00'), ('00:00', '00:00'), ('09:00', '09:00')], default='00:00', max_length=10),
        ),
    ]
