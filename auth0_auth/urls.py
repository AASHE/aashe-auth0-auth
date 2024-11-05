from django.urls import include, path

urlpatterns = [
    path("", include("mozilla_django_oidc.urls")),
]
