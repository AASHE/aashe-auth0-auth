# AASHE Auth0 Auth

Allows AASHE applications to authenticate through Auth0.

This project uses `mozilla-django-oidc` under the hood.

## Installation

Install the package:

```
pip install git+https://github.com/aashe/aashe-auth0-auth.git@master
```

Add the Auth0Backend to your AUTHENTICATION_BACKENDS setting:

```
AUTHENTICATION_BACKENDS = (
    ...
    'auth0_auth.backends.Auth0Backend',
)
```

Edit your urls.py to include:

```
urlpatterns = [
    path(r'^auth0/', include('auth0_auth.urls')),
    ...
]
```

## Settings

Add the required env vars and settings

```
BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8080")
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", )
OIDC_RP_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
OIDC_RP_SCOPES = os.environ.get("OIDC_RP_SCOPES", "openid profile email")

CUSTOM_OIDC_GROUPS_CLAIM = "https://accounts-aashe.aashe.org/roles"
AUTH0_LOGOUT_ENDPOINT = f"https://{AUTH0_DOMAIN}/v2/logout"
ALLOW_LOGOUT_GET_METHOD = True
LOGIN_REDIRECT_URL = f"{BASE_URL}/django-admin/"
LOGOUT_REDIRECT_URL = f"{BASE_URL}/django-admin/logout/"
OIDC_OP_JWKS_ENDPOINT = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
OIDC_RP_SIGN_ALGO = "RS256"
OIDC_OP_LOGOUT_URL_METHOD = "aashe_accounts.support.oidc_helpers.provider_logout"
# So we can configure it dynamically
try:
    document = requests.get(f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration").json()
    OIDC_OP_AUTHORIZATION_ENDPOINT = document["authorization_endpoint"]
    OIDC_OP_TOKEN_ENDPOINT = document["token_endpoint"]
    OIDC_OP_USER_ENDPOINT = document["userinfo_endpoint"]
except requests.exceptions.ConnectionError:
    print("Skipping configuration for OIDC! It won't work correctly")
    OIDC_OP_AUTHORIZATION_ENDPOINT = None
    OIDC_OP_TOKEN_ENDPOINT = None
    OIDC_OP_USER_ENDPOINT = None
OIDC_VERIFY_SSL = True

```
