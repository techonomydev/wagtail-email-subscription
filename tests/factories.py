import factory
import wagtail_factories
from django.conf import settings
from wagtail.core.models import Locale, Page
from wagtail.core.utils import get_supported_content_language_variant

from wagtail_email_subscription.contrib.formpage.models import (
    FormPage,
    FormPageField,
    FormPageSubmission,
)
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

    form_page = factory.SubFactory("tests.factories.FormPageFactory")
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


class LocaleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Locale

    language_code = get_supported_content_language_variant(settings.LANGUAGE_CODE)


class SiteFactory(wagtail_factories.SiteFactory):
    hostname = "localhost"
    port = 8000
    site_name = "My Wagtail Email Subscription Test Site"
    is_default_site = True
    root_page = factory.SubFactory(FormPageFactory)
    settings = factory.RelatedFactory(
        EmailSubscriptionSettingsFactory, factory_related_name="site"
    )


class FormPageSubmissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FormPageSubmission

    form_data = '{"email": "test@test.com"}'
    page = factory.SubFactory(FormPageFactory)
