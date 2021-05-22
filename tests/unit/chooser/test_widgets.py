import pytest
from django.core.exceptions import ObjectDoesNotExist

from wagtail_email_subscription.chooser.widgets import ListChooserWidget


@pytest.mark.django_db
def test_list_chooser_widget_site_url(wagtail_site):
    widget = ListChooserWidget(page_instance=wagtail_site.root_page)

    # make sure the url is correctly reversed to the right view, including
    # the site_id
    url = widget.get_choose_modal_url()
    assert url is not None
    assert url == f"/admin/active-campaign-lists/?site_id={wagtail_site.pk}"


def test_list_chooser_widget_get_instance():
    widget = ListChooserWidget()

    with pytest.raises(ObjectDoesNotExist):
        # as this widget is used with a JSON field, A None value is parsed
        # as 'null'
        widget.get_instance("null")

    instance = widget.get_instance('{"id": "id", "title": "title"}')
    assert isinstance(instance, dict)
    assert "id" in instance
    assert "title" in instance

    instance = widget.get_instance('{"id": "id", "title": "title"}')
    assert isinstance(instance, dict)
    assert "id" in instance
    assert "title" in instance


def test_list_chooser_widget_get_title(wagtail_site):
    widget = ListChooserWidget()

    title = widget.get_title({"id": "id", "title": "title"})
    assert isinstance(title, str)
    assert title == "title"

    # when no title key is available, return an empty string
    title = widget.get_title({"id": "id"})
    assert isinstance(title, str)
    assert title == ""
