from wagtail.admin.edit_handlers import FieldPanel, ObjectList, TabbedInterface
from wagtail.core.fields import RichTextField

from wagtail_active_campaign.models import ActiveCampaignForm


class FormPage(ActiveCampaignForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = ActiveCampaignForm.content_panels + [
        FieldPanel("intro", classname="full"),
        FieldPanel("thank_you_text", classname="full"),
    ]
    parent_page_types = ["wagtailcore.Page"]
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Form"),
            ObjectList(ActiveCampaignForm.submission_panels, heading="Submissions"),
            ObjectList(ActiveCampaignForm.promote_panels, heading="Promote"),
            ObjectList(ActiveCampaignForm.settings_panels, heading="Settings"),
        ]
    )
    template = "wagtail_active_campaign/form_page.html"
