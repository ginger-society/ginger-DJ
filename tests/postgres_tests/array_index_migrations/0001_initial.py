import ginger.contrib.postgres.fields
from ginger.db import migrations, models


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CharTextArrayIndexModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "char",
                    ginger.contrib.postgres.fields.ArrayField(
                        models.CharField(max_length=10), db_index=True, size=100
                    ),
                ),
                ("char2", models.CharField(max_length=11, db_index=True)),
                (
                    "text",
                    ginger.contrib.postgres.fields.ArrayField(
                        models.TextField(), db_index=True
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]
