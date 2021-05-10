import pytest
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_settings(email_subscription_setttings):
    assert email_subscription_setttings.clean() is None

    email_subscription_setttings.api_key = "invalid-api-key"
    with pytest.raises(ValidationError):
        email_subscription_setttings.clean()

    # when disabled, the validation in the clean method will pass
    email_subscription_setttings.api_key = "invalid-api-key"
    email_subscription_setttings.enabled = False
    assert email_subscription_setttings.clean() is None


@pytest.mark.django_db
def test_page_form_process_form_submission(wagtail_site, mocker):
    patched = mocker.patch(
        "wagtail_email_subscription.abstract_models.AbstractEmailSubscriptionFormSubmission.handle_email_subscription_submission"
    )
    # Configure the page so that handle_email_subscription_submission is NOT called
    page = wagtail_site.root_page
    page.enabled = False
    page.save()

    form = page.get_form(data={"email": "test@test.comn"})
    assert form.is_valid()
    submission_instance = page.process_form_submission(form)
    assert isinstance(submission_instance, page.get_submission_class())
    assert patched.called is False

    # Let's configure the page so handle_email_subscription_submission will be called
    page.selected_list = "1"
    page.enabled = True
    page.save()

    submission_instance = page.process_form_submission(form)
    assert patched.called is True


@pytest.mark.django_db
def test_page_form_get_form_fields(wagtail_site):
    page = wagtail_site.root_page
    # default, the page is created with a single form field
    assert page.get_form_fields().count() == 1

    page.get_form_fields().delete()
    assert page.get_form_fields().count() == 0


@pytest.mark.django_db
def test_page_form_get_chosen_mapping_fields(wagtail_site):
    page = wagtail_site.root_page

    # Returns all fields which contain a mapping
    page.get_chosen_mapping_fields()
    assert page.get_chosen_mapping_fields().first() == "email"

    # No mapping, no glory
    page.get_form_fields().filter(clean_name="email").update(mapping="")
    assert page.get_chosen_mapping_fields().count() == 0


@pytest.mark.django_db
def test_page_form_get_data_fields(wagtail_site):
    page = wagtail_site.root_page

    # we expect here submit_time,  email and  synced fields here
    assert len(page.get_data_fields()) == 3

    page.get_form_fields().delete()
    assert len(page.get_data_fields()) == 2


@pytest.mark.django_db
def test_page_form_submission_data(form_page_submission):
    data = form_page_submission.get_data()
    assert list(data.keys()) == ["email", "submit_time", "synced"]

    form_page_submission.form_data = '{"another_field": "value"}'
    form_page_submission.save()

    data = form_page_submission.get_data()
    assert list(data.keys()) == ["another_field", "submit_time", "synced"]
