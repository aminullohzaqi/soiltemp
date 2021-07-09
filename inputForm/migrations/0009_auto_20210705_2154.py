# Generated by Django 3.1.3 on 2021-07-05 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inputForm', '0008_auto_20210705_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soiltempmodel',
            name='jam',
            field=models.CharField(choices=[('01:00', '01:00'), ('14:00', '14:00'), ('05:00', '05:00'), ('11:00', '11:00'), ('04:00', '04:00'), ('02:00', '02:00'), ('07:00', '07:00'), ('10:00', '10:00'), ('00:00', '00:00'), ('12:00', '12:00'), ('03:00', '03:00'), ('13:00', '13:00'), ('09:00', '09:00'), ('15:00', '15:00'), ('16:00', '16:00'), ('06:00', '06:00'), ('08:00', '08:00'), ('17:00', '17:00')], default='00:00', max_length=10),
        ),
        migrations.AlterField(
            model_name='soiltempmodelcilacap',
            name='jam',
            field=models.CharField(choices=[('12:00', '12:00'), ('00:00', '00:00'), ('03:00', '03:00'), ('06:00', '06:00'), ('09:00', '09:00')], default='00:00', max_length=10),
        ),
    ]