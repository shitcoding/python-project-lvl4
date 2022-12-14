# Generated by Django 4.1 on 2022-10-27 21:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("task_manager", "0002_remove_task_labels_task_label"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="label",
            options={"verbose_name": "Label"},
        ),
        migrations.AlterModelOptions(
            name="siteuser",
            options={"verbose_name": "User"},
        ),
        migrations.AlterModelOptions(
            name="status",
            options={"verbose_name": "Status"},
        ),
        migrations.AlterModelOptions(
            name="task",
            options={"verbose_name": "Task"},
        ),
        migrations.AlterField(
            model_name="label",
            name="created_on",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Created on"),
        ),
        migrations.AlterField(
            model_name="label",
            name="name",
            field=models.CharField(max_length=30, unique=True, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="siteuser",
            name="first_name",
            field=models.CharField(max_length=30, verbose_name="First name"),
        ),
        migrations.AlterField(
            model_name="siteuser",
            name="last_name",
            field=models.CharField(max_length=30, verbose_name="Last name"),
        ),
        migrations.AlterField(
            model_name="siteuser",
            name="signup_date",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Signup date"),
        ),
        migrations.AlterField(
            model_name="siteuser",
            name="username",
            field=models.CharField(max_length=30, unique=True, verbose_name="Username"),
        ),
        migrations.AlterField(
            model_name="status",
            name="created_on",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Created on"),
        ),
        migrations.AlterField(
            model_name="status",
            name="name",
            field=models.CharField(max_length=30, unique=True, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="task",
            name="created_on",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Created on"),
        ),
        migrations.AlterField(
            model_name="task",
            name="creator",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="creator",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Creator",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="description",
            field=models.TextField(max_length=5000, verbose_name="Description"),
        ),
        migrations.AlterField(
            model_name="task",
            name="label",
            field=models.ManyToManyField(
                related_name="tasks", to="task_manager.label", verbose_name="Label"
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="name",
            field=models.CharField(max_length=100, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="task",
            name="performer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="performer",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Performer",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="status",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="task_manager.status",
                verbose_name="Status",
            ),
        ),
    ]
