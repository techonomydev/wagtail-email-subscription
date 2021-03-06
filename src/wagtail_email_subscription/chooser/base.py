import json
from urllib.parse import urlencode

from django.core.exceptions import ObjectDoesNotExist
from django.urls import path, re_path
from generic_chooser.views import ChooserMixin, ChooserViewSet
from wagtail.core.models import Site

from wagtail_email_subscription.utils import get_email_subscription_settings


class EmailSubscriptionChooserMixin(ChooserMixin):
    is_searchable = False
    per_page = 10

    id_field = "id"
    title_field = "name"

    def filter_result_by_search_term(self, result, search_term):
        return [x for x in result if search_term.lower() in x[self.title_field].lower()]

    def call_client(self, client):
        raise NotImplementedError(
            "Implement a call_client method in the specific viewset"
        )

    def get_object_list(self, search_term=None, **kwargs):  # pylint: disable=W0221
        result = []

        site_id = self.request.GET.get("site_id", None)
        site = Site.objects.filter(id=site_id).first()

        if site is None:
            return result

        settings = get_email_subscription_settings(site)

        if settings.enabled:
            client = settings.get_client()

            if client.check_credentials():
                result = self.call_client(client)
            if search_term:
                result = self.filter_result_by_search_term(result, search_term)
        return result

    def get_object(self, item_id):  # pylint: disable=W0221,W0237
        all_items = self.get_object_list()
        selected_object = next(
            (item for item in all_items if item[self.id_field] == item_id), None
        )
        if not selected_object:
            raise ObjectDoesNotExist(str(item_id))
        return selected_object

    def get_object_id(self, item):  # pylint: disable=W0221,W0237
        return item[self.id_field]

    def get_object_string(self, item):  # pylint: disable=W0221,W0237
        return f"{item[self.title_field]}"

    def get_choose_url(self):
        choose_url = super().get_choose_url()
        url_param = urlencode(self.request.GET)
        return f"{choose_url}?{url_param}" if url_param else choose_url

    def get_chosen_url(self, instance):
        chosen_url = super().get_chosen_url(instance)
        url_param = urlencode(self.request.GET)
        return f"{chosen_url}?{url_param}" if url_param else chosen_url

    def get_chosen_response_data(self, item):
        return {
            "id": json.dumps(
                {"id": item[self.id_field], "title": item[self.title_field]}
            ),
            "string": self.get_object_string(item),
            "edit_link": self.get_edit_item_url(item),
        }


class EmailSubscriptionChooserViewSet(ChooserViewSet):
    chooser_mixin_class = EmailSubscriptionChooserMixin

    def update_attrs(self, attrs):
        override_attributes = (
            "call_client",
            "filter_result_by_search_term",
            "get_object_string",
            "id_field",
            "title_field",
            "is_searchable",
        )
        for attr in override_attributes:
            if hasattr(self, attr):
                attrs[attr] = getattr(self, attr)
        return attrs

    def get_choose_view_attrs(self):
        attrs = super().get_choose_view_attrs()
        return self.update_attrs(attrs)

    def get_chosen_view_attrs(self):
        attrs = super().get_chosen_view_attrs()
        return self.update_attrs(attrs)

    def get_urlpatterns(self):
        return [
            path("", self.choose_view, name="choose"),
            # we override this because our "id's" can also be slug
            # like values so we need a different regex here
            re_path(r"^([-\w.]+)/$", self.chosen_view, name="chosen"),
        ]
