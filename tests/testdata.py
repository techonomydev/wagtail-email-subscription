# all these outputs are simplified to be the bare minimum needed for our testsuite

LIST_OUTPUT = {
    "lists": [
        {
            "stringid": "my-list",
            "id": "1",
            "name": "My list",
        },
        {
            "stringid": "another-list",
            "id": "2",
            "name": "Another list",
        },
    ]
}

CREATE_UPDATE_CONTACT_OUTPUT = {
    "contact": {
        "id": "1",
        "email": "test@test.com",
        "phone": "",
        "firstName": "First Name",
        "lastName": "Lastt Name",
    }
}

UPDATE_LIST_STATUS_OUTPUT = {"contactList": {"contact": "1", "list": "1"}}

UPDATE_LIST_STATUS_ERROR = {
    "errors": [
        {
            "title": "The related list does not exist.",
            "detail": "",
            "code": "related_missing",
            "error": "list_not_exist",
            "source": {"pointer": "/data/attributes/list"},
        }
    ]
}
