from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.core.fields import RichTextField

from wagtail_email_subscription.abstract_models import (
    AbstractEmailSubscriptionForm,
    AbstractEmailSubscriptionFormField,
    AbstractEmailSubscriptionFormSubmission,
)


class FormPageSubmission(AbstractEmailSubscriptionFormSubmission):
    pass


class FormPage(AbstractEmailSubscriptionForm):
    FORM_FIELD = "form_page"
    FORM_FIELDS_REVERSE = "form_page_fields"

    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailSubscriptionForm.content_panels + [
        FieldPanel("intro", classname="full"),
        InlinePanel(FORM_FIELDS_REVERSE, label="form fields"),
        FieldPanel("thank_you_text", classname="full"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Form"),
            ObjectList(
                AbstractEmailSubscriptionForm.submission_panels, heading="Submissions"
            ),
            ObjectList(AbstractEmailSubscriptionForm.promote_panels, heading="Promote"),
            ObjectList(
                AbstractEmailSubscriptionForm.settings_panels, heading="Settings"
            ),
        ]
    )

    template = "form_page/form_page.html"

    def get_submission_class(self):
        return FormPageSubmission


class FormPageField(AbstractEmailSubscriptionFormField):
    form_page = ParentalKey(
        "FormPage", on_delete=models.CASCADE, related_name="form_page_fields"
    )
