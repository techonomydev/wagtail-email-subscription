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

from .chooser.panels import EmailSubscriptionListPanel
from .utils import get_email_subscription_settings

logger = logging.getLogger(__name__)


class AbstractEmailSubscriptionFormSubmission(AbstractFormSubmission):
    PAGE_FIELD = "page"

    synced = models.BooleanField(
        "Synced",
        help_text="This record is synced with the Email Subscription Provider",
        default=False,
    )

    class Meta(AbstractFormSubmission.Meta):
        abstract = True

    def get_data(self):
        data = super().get_data()
        return {**data, "synced": self.synced}

    def handle_email_subscription_submission(self):
        prepared_data = self.prepare_data_for_subscription_provider()

        if prepared_data == {} or "email" not in prepared_data:
            logger.error("The required email field is not in the formdata!")
        else:
            self.post_data_to_subscription_provider()

    def prepare_data_for_subscription_provider(self):
        data = self.get_data()
        page = getattr(self, self.PAGE_FIELD).specific  # pylint: disable=no-member

        # only use the fields which have a filled out mapping field
        qs = getattr(page, page.FORM_FIELDS_REVERSE)
        qs = qs.exclude(mapping__exact="")
        qs = qs.values_list("mapping", "clean_name")

        return {mapping: data[clean_name] for mapping, clean_name in qs}

    def post_data_to_subscription_provider(self):
        page = getattr(self, self.PAGE_FIELD).specific  # pylint: disable=no-member
        site = page.get_site()

        settings = get_email_subscription_settings(site)

        if not settings.enabled:
            logger.warning("The Email Subscription Provider is not enabled!")
            return

        client = settings.get_client()

        if not client.check_credentials():
            logger.error(
                "The Email Subscription Provider credentials are not set correctly!"
            )
            return

        data = self.prepare_data_for_subscription_provider()

        logger.debug("Posting %s to active campaign", data)
        contact = client.create_or_update_subscriber(data)
        logger.debug("Contact added: %s", contact["id"])

        logger.debug("Adding contact %s to list %s", contact["id"], page.selected_list)
        client.add_subscriber_to_list(
            contact_id=contact["id"], list_id=page.selected_list
        )
        logger.debug("Contact %s added to list %s", contact["id"], page.selected_list)

        self.synced = True
        self.save()


class AbstractEmailSubscriptionForm(AbstractForm):
    FORM_FIELD = "form"
    FORM_FIELDS_REVERSE = "form_fields"

    enabled = models.BooleanField(
        "Enabled",
        help_text="Enable or disable the Email Subscription integration of this form",
        default=False,
    )
    selected_list = models.CharField(
        "List",
        max_length=255,
        blank=True,
        help_text="Select the Email Subscription list where the new subscribers will be a member of after submission",
    )

    settings_panels = AbstractForm.settings_panels + [
        MultiFieldPanel(
            [
                FieldPanel("enabled"),
                EmailSubscriptionListPanel("selected_list"),
            ],
            heading="Email Subscription Settings",
        ),
    ]

    submission_panels = [
        FormSubmissionsPanel(),
    ]

    content_panels = AbstractForm.content_panels

    class Meta(AbstractForm.Meta):
        abstract = True

    def process_form_submission(self, form):
        instance = super().process_form_submission(form)

        if self.enabled:
            instance.handle_email_subscription_submission()

        return instance

    def get_form_fields(self):
        return getattr(self, self.FORM_FIELDS_REVERSE).all()

    def get_chosen_mapping_fields(self):
        qs = getattr(self, self.FORM_FIELDS_REVERSE)
        qs = qs.exclude(mapping__exact="")
        return qs.values_list("mapping", flat=True)

    def clean(self):
        super().clean()

        if self.enabled and not self.selected_list:
            raise ValidationError(
                {
                    "selected_list": "Please select a valid list when the Email Subscription is enabled"
                }
            )

    def get_data_fields(self):
        fields = super().get_data_fields()
        return fields + [("synced", "Synced")]


class AbstractEmailSubscriptionFormField(AbstractFormField):
    # TODO: Make this a setting and/or dynamic, or query them in the site settings and
    # store them
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
        help_text="Select the mapped Email Subscription field",
        choices=ACTIVE_CAMPAIN_FIELDNAMES,
    )

    panels = AbstractFormField.panels + [FieldPanel("mapping")]

    class Meta(AbstractFormField.Meta):
        abstract = True


AbstractEmailSubscriptionFormField.base_form_class = None
