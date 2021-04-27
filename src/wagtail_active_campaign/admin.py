# empty file
from django.contrib import admin

from .models import ActiveCampaignForm, ActiveCampaignFormField, ActiveCampaignSettings


class ActiveCampaignFormFieldInline(admin.TabularInline):
    model = ActiveCampaignFormField


class ActiveCampaignFormPageAdmin(admin.ModelAdmin):
    inlines = [
        ActiveCampaignFormFieldInline,
    ]


admin.site.register(ActiveCampaignForm, ActiveCampaignFormPageAdmin)
admin.site.register(ActiveCampaignSettings)
