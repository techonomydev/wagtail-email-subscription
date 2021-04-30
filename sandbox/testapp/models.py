from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.core.fields import RichTextField

from wagtail_active_campaign.abstract_models import (
    AbstractActiveCampaignForm,
    AbstractActiveCampaignFormField,
)


class FormPage(AbstractActiveCampaignForm):
    FORM_FIELD = "form_page"
    FORM_FIELDS_REVERSE = "form_page_fields"

    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractActiveCampaignForm.content_panels + [
        FieldPanel("intro", classname="full"),
        InlinePanel(FORM_FIELDS_REVERSE, label="form fields"),
        FieldPanel("thank_you_text", classname="full"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Form"),
            ObjectList(
                AbstractActiveCampaignForm.submission_panels, heading="Submissions"
            ),
            ObjectList(AbstractActiveCampaignForm.promote_panels, heading="Promote"),
            ObjectList(AbstractActiveCampaignForm.settings_panels, heading="Settings"),
        ]
    )

    template = "wagtail_active_campaign/form_page.html"


class FormPageFormField(AbstractActiveCampaignFormField):
    form_page = ParentalKey(
        "FormPage", on_delete=models.CASCADE, related_name="form_page_fields"
    )

    class Meta(AbstractActiveCampaignFormField.Meta):
        constraints = (
            models.UniqueConstraint(
                name="A mapping field can only be used once for each form",
                fields=(FormPage.FORM_FIELD, "mapping"),
            ),
        )
