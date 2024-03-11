from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_organization'),
        ('ambulance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ambulance',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='login.Organization', verbose_name='Organization'),
        ),

    ]