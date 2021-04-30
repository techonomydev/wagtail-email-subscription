from django.contrib import admin

from .models import FormPage, FormPageField


class FormFieldInline(admin.TabularInline):
    model = FormPageField


@admin.register(FormPage)
class ActiveCampaignFormPageAdmin(admin.ModelAdmin):
    inlines = [
        FormFieldInline,
    ]


admin.site.register(FormPage().get_submission_class())
