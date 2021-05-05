import pytest

from wagtail_email_subscription.chooser.widgets import ListChooserWidget


@pytest.mark.django_db
def test_list_chooser_widget(wagtail_site):
    widget = ListChooserWidget(page_instance=wagtail_site.root_page)

    # make sure the url is correctly reversed to the right view, including
    # the site_id
    url = widget.get_choose_modal_url()
    assert url is not None
    assert url == f"/admin/active-campaign-lists/?site_id={wagtail_site.pk}"
