from django.urls import include, path
from auth0_auth.api_views import api

urlpatterns = [
    path("", include("mozilla_django_oidc.urls")),
    path("api/", api.urls),
]
