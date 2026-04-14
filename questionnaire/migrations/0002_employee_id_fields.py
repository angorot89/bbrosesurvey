from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='id_number',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='employee',
            name='id_type',
            field=models.CharField(blank=True, default='id', max_length=20),
        ),
    ]
