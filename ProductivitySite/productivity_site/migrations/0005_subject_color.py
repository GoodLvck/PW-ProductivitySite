# Generated manually because the local Django environment is not available.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("productivity_site", "0004_rename_fill_blanks_fillblanks_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subject",
            name="subject_id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name="subject",
            name="color",
            field=models.CharField(default="#f59e0b", max_length=7),
        ),
    ]
