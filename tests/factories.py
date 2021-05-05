import factory
import wagtail_factories
from wagtail.core.models import Page

from wagtail_email_subscription.contrib.formpage.models import FormPage, FormPageField
from wagtail_email_subscription.models import EmailSubscriptionSettings


class EmailSubscriptionSettingsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmailSubscriptionSettings

    api_url = "https://valid-server.api.activecampaign.com"
    api_key = "my-api-key"
    enabled = True


class FormPageFieldFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FormPageField

    clean_name = "email"
    label = "Email"
    field_type = "email"
    mapping = "email"


class FormPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = FormPage

    title = "My Form Page"
    form_page_fields = factory.RelatedFactory(
        FormPageFieldFactory,
        factory_related_name="form_page",
    )

    @factory.lazy_attribute
    def parent(self):
        return Page.get_first_root_node()


class SiteFactory(wagtail_factories.SiteFactory):
    hostname = "localhost"
    port = 8000
    site_name = "My Wagtail Email Subscription Test Site"
    is_default_site = False
    root_page = factory.SubFactory(FormPageFactory)
    settings = factory.RelatedFactory(
        EmailSubscriptionSettingsFactory, factory_related_name="site"
    )
