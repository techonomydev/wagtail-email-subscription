import json

import pytest
from django.urls import reverse

from tests import testdata


@pytest.mark.django_db
def test_choose_list_choose_unauthorized(client):
    choose_url = reverse("list_chooser:choose")
    response = client.get(choose_url)
    assert response.status_code == 302
    assert "login" in response["location"]


@pytest.mark.django_db
def test_choose_list_chosen_unauthorized(client):
    chosen_url = reverse("list_chooser:chosen", args=(1,))
    response = client.get(chosen_url)
    assert response.status_code == 302
    assert "login" in response["location"]


@pytest.mark.django_db
def test_choose_list_choose(wagtail_site, admin_client):
    choose_url = reverse("list_chooser:choose")
    choose_url = f"{choose_url}?site_id={wagtail_site.pk}"
    response = admin_client.get(choose_url)
    assert response.status_code == 200
    assert "html" in response.json()

    html_snippet = response.json()["html"]

    # Make sure the form POST url includes the site_id
    assert (
        f'data-action-url="/admin/active-campaign-lists/?site_id={wagtail_site.pk}"'
        in html_snippet
    )

    # Mke sure the lists defined in testdata.LIST_OUTPUT are returned here including
    # the correct site_id
    for item in testdata.LIST_OUTPUT["lists"]:
        assert (
            f'href="/admin/active-campaign-lists/{item["id"]}/?site_id={wagtail_site.pk}'
            in html_snippet
        )


@pytest.mark.django_db
def test_chosen_list_chosen(wagtail_site, admin_client):
    # The chosen view should return the correct selected data in the chooser, aka
    # the "chosen" values
    for item in testdata.LIST_OUTPUT["lists"]:
        chosen_url = reverse("list_chooser:chosen", args=(item["id"],))
        response = admin_client.get(f"{chosen_url}?site_id={wagtail_site.pk}")
        assert response.status_code == 200

        result = response.json()
        assert "result" in result

        parsed = json.loads(result["result"]["id"])
        assert parsed["id"] == item["id"]
        assert parsed["title"] == item["name"]
