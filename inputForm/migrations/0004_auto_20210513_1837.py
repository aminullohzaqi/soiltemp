# Generated by Django 3.1.3 on 2021-05-13 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inputForm', '0003_auto_20210513_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soiltempmodel',
            name='jam',
            field=models.CharField(choices=[('03:00', '03:00'), ('12:00', '12:00'), ('09:00', '09:00'), ('06:00', '06:00'), ('00:00', '00:00')], default='00:00', max_length=10),
        ),
        migrations.AlterField(
            model_name='soiltempmodelcilacap',
            name='jam',
            field=models.CharField(choices=[('03:00', '03:00'), ('12:00', '12:00'), ('09:00', '09:00'), ('06:00', '06:00'), ('00:00', '00:00')], default='00:00', max_length=10),
        ),
    ]
