from django.contrib import admin

from .models import FormPage, FormPageField, FormPageSubmission


class FormFieldInline(admin.TabularInline):
    model = FormPageField


@admin.register(FormPage)
class FormPageAdmin(admin.ModelAdmin):
    inlines = [
        FormFieldInline,
    ]


admin.site.register(FormPageSubmission)
