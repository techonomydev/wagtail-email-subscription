import pytest

from tests.factories import FormPageFactory, FormPageFieldFactory


@pytest.mark.django_db
def test_page_form_multiple_form_fields(wagtail_site):

    form_page = FormPageFactory(parent=wagtail_site.root_page, title="Another form")

    FormPageFieldFactory(
        form_page=form_page,
        label="First Name",
        field_type="singleline",
        mapping="firstName",
    )
    FormPageFieldFactory(
        form_page=form_page,
        label="Last Name",
        field_type="singleline",
        mapping="lastName",
    )
    FormPageFieldFactory(
        form_page=form_page,
        label="Notes",
        field_type="multiline",
        mapping="",
    )
    FormPageFieldFactory(
        form_page=form_page,
        label="Remark",
        field_type="singleline",
        mapping="",
    )

    form_page_fields = getattr(form_page, form_page.FORM_FIELDS_REVERSE)
    # including the original email fields
    assert form_page_fields.count() == 5

    clean_names = form_page_fields.values_list("clean_name", flat=True)
    assert ["email", "first_name", "last_name", "notes", "remark"] == list(clean_names)
    assert form_page.clean() is None
