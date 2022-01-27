# Generated by Django 3.1.8 on 2021-05-11 12:22

from django.db import migrations, models
import json


def convert_to_json(apps, schema_editor):
    FormPage = apps.get_model("formpage", "FormPage")

    for form in FormPage.objects.all():
        if form.selected_list is not None:
            form.selected_list = '{"id": "%s", "title": "%s"}' % (form.selected_list, form.selected_list)
            form.save()
            form.revisions.all().delete()


def convert_to_charfield(apps, schema_editor):
    FormPage = apps.get_model("formpage", "FormPage")

    for form in FormPage.objects.all():
        if form.selected_list is None:
            continue

        selected_list = json.loads(form.selected_list)

        if isinstance(selected_list, dict) and "id" in selected_list:
            form.selected_list = json.loads(form.selected_list)["id"]
            form.save()
        form.revisions.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('formpage', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(convert_to_json, reverse_code=convert_to_charfield),
        migrations.AlterField(
            model_name='formpage',
            name='selected_list',
            field=models.JSONField(blank=True, null=True, help_text='Select the Email Subscription list where the new subscribers will be a member of after submission', verbose_name='List'),
        ),
    ]