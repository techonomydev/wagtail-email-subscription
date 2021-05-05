import pytest

from wagtail_email_subscription.contrib.formpage.models import FormPageSubmission


@pytest.mark.django_db
def test_form_view(wagtail_site, client):
    assert FormPageSubmission.objects.count() == 0  # pylint: disable=no-member

    # enable the submission via the api
    wagtail_site.root_page.selected_list = "1"
    wagtail_site.root_page.enabled = True
    wagtail_site.root_page.save()

    # Actually fill out the form and check if the subscription is actually submitted
    response = client.get(wagtail_site.root_url)
    assert response.status_code == 200

    response = client.post(wagtail_site.root_url, data={"email": "email@test.com"})
    assert response.status_code == 200

    # Check if the submission is there
    assert FormPageSubmission.objects.count() == 1  # pylint: disable=no-member
