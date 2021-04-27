from django.http import HttpResponse


def index(request):
    return HttpResponse(
        f"This is the wagtail-active-campaign boilerplate view on {request.get_full_path()}"
    )
