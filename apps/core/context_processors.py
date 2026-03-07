from django.conf import settings

def theme(request):
    return {
        "THEME": settings.THEME
    }

def breadcrumbs(request):

    breadcrumbs = []

    if request.resolver_match:
        url_name = request.resolver_match.url_name

        if url_name:
            parts = url_name.split("_")

            for part in parts:
                breadcrumbs.append({
                    "name": part.capitalize(),
                    "url": ""
                })

    return {
        "breadcrumbs": breadcrumbs
    }
