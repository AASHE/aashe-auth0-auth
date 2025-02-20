import time
from django.contrib import auth
from mozilla_django_oidc.views import OIDCAuthenticationCallbackView
from auth0_auth.api_client import AASHEAccountsAPIClient
from django.http import HttpResponseRedirect

class GetUserProfileCallbackView(OIDCAuthenticationCallbackView):

    def login_success(self):
        # If the user hasn't changed (because this is a session refresh instead of a
        # normal login), don't call login. This prevents invaliding the user's current CSRF token
        request_user = getattr(self.request, "user", None)
        if (
            not request_user
            or not request_user.is_authenticated
            or request_user != self.user
        ):
            # get user profile and access data and store it in the session
            accounts_client = AASHEAccountsAPIClient()
            resp = accounts_client.get_user_profile(self.user.username)
            if resp.status_code == 200:
                self.request.session["user_profile"] = resp.json()
                auth.login(self.request, self.user)
            else:
                print(resp)

        # Figure out when this id_token will expire. This is ignored unless you're
        # using the SessionRefresh middleware.
        expiration_interval = self.get_settings(
            "OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS", 60 * 15
        )
        self.request.session["oidc_id_token_expiration"] = (
            time.time() + expiration_interval
        )

        return HttpResponseRedirect(self.success_url)
