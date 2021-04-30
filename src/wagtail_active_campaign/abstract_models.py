import logging

from django.core.exceptions import ValidationError
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from wagtail.contrib.forms.models import (
    AbstractForm,
    AbstractFormField,
    AbstractFormSubmission,
)

from .chooser.widgets import ListChooserWidget
from .utils import get_active_campaign_settings

logger = logging.getLogger(__name__)


class AbstractActiveCampaignFormSubmission(AbstractFormSubmission):
    PAGE_FIELD = "page"

    synced = models.BooleanField(
        "Synced",
        help_text="This record is synced with Active Campaign",
        default=False,
    )

    class Meta(AbstractFormSubmission.Meta):
        abstract = True

    def handle_active_campaign_submission(self):
        prepared_data = self.prepare_data_for_active_campain()

        if prepared_data == {} or "email" not in prepared_data:
            page = getattr(self, self.PAGE_FIELD)
            logger.error("%s The required email field is not in the formdata!", page)
        else:
            self.post_data_to_active_campaign(prepared_data)

    def prepare_data_for_active_campain(self):
        data = self.get_data()
        page = getattr(self, self.PAGE_FIELD)

        # only use the fields which have a filled out mapping field
        qs = getattr(page, page.FORM_FIELDS_REVERSE)
        qs = qs.exclude(mapping__exact="")
        qs = qs.values_list("mapping", "clean_name")

        return {mapping: data[clean_name] for mapping, clean_name in qs}

    def post_data_to_active_campaign(self, data):
        page = getattr(self, self.PAGE_FIELD)
        site = page.get_site()
        settings = get_active_campaign_settings(site)

        if not settings.enabled:
            logger.warning("Check your settings as Active Campaign is not enabled!")
            return

        client = settings.get_client()

        if not client.check_credentials():
            logger.error("Active Campaign credentials are not set correctly!")
            return

        logger.debug("Posting %s to active campaign", data)
        contact = client.create_or_update_contact(data)
        logger.debug("Contact added: %s", contact["id"])

        logger.debug("Adding contact %s to list %s", contact["id"], page.selected_list)
        client.add_contact_to_list(contact_id=contact["id"], list_id=page.selected_list)
        logger.debug("Contact %s added to list %s", contact["id"], page.selected_list)

        self.synced = True
        self.save()


class AbstractActiveCampaignForm(AbstractForm):
    FORM_FIELD = "form"
    FORM_FIELDS_REVERSE = "form_fields"

    enabled = models.BooleanField(
        "Enabled",
        help_text="Enable or disable the Active Campaign integration of this form",
        default=False,
    )
    selected_list = models.CharField(
        "List",
        max_length=255,
        blank=True,
        help_text="Select the Active Campaign list where the new subscribers will be a member of after submission",
    )

    settings_panels = AbstractForm.settings_panels + [
        MultiFieldPanel(
            [
                FieldPanel("enabled"),
                FieldPanel("selected_list", widget=ListChooserWidget),
            ],
            heading="Active Campaign settings",
        ),
    ]

    submission_panels = [
        FormSubmissionsPanel(),
    ]

    content_panels = AbstractForm.content_panels

    template = "wagtail_active_campaign/form_page.html"

    class Meta(AbstractForm.Meta):
        abstract = True

    def process_form_submission(self, form):
        instance = super().process_form_submission(form)

        if self.enabled:
            instance.handle_active_campaign_submission()

        return instance

    def get_form_fields(self):
        return getattr(self, self.FORM_FIELDS_REVERSE).all()

    def clean(self):
        super().clean()

        if self.enabled and not self.selected_list:
            raise ValidationError(
                {
                    "selected_list": "Please select a valid list when the Active Campaign is enabled"
                }
            )


class AbstractActiveCampaignFormField(AbstractFormField):
    # TODO: Make this a setting and/or dynamic
    ACTIVE_CAMPAIN_FIELDNAMES = (
        ("email", "email"),
        ("firstName", "firstName"),
        ("lastName", "lastName"),
        ("phone", "phone"),
    )

    mapping = models.CharField(
        "Map field to",
        max_length=255,
        blank=True,
        help_text="Select the mapped Active Campaign field",
        choices=ACTIVE_CAMPAIN_FIELDNAMES,
    )

    panels = AbstractFormField.panels + [FieldPanel("mapping")]

    class Meta(AbstractFormField.Meta):
        abstract = True
