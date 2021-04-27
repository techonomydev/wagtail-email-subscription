from django.urls import reverse


def test_root_view(client):
    url = reverse("wagtail_active_campaign:index")
    response = client.get(url)
    assert response.status_code == 200
