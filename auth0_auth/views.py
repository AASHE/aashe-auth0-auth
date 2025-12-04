import time, logging
from django.contrib import auth
from mozilla_django_oidc.views import OIDCAuthenticationCallbackView
from auth0_auth.api_client import AASHEAccountsAPIClient
from django.http import HttpResponseRedirect

logger = logging.getLogger(__name__)

class GetUserProfileCallbackView(OIDCAuthenticationCallbackView):

    def login_success(self):
        # If the user hasn't changed (because this is a session refresh instead of a # normal login), don't call login. 
        # This prevents invaliding the user's current CSRF token
        request_user = getattr(self.request, "user", None)
        is_refresh = (
            request_user 
            and request_user.is_authenticated 
            and request_user == self.user
        )

        if not is_refresh:
            accounts_client = AASHEAccountsAPIClient()

            try:
                resp = accounts_client.get_user_profile(self.user.username)
            except Exception as e:
                logger.exception(f"Failed to call Accounts API for user={self.user.username}")
                return HttpResponseRedirect(self.failure_url)

            if resp.status_code == 200:
                try:
                    profile = resp.json()
                except Exception:
                    logger.error(
                        "Invalid JSON from Accounts API",
                        extra={
                            "username": self.user.username,
                            "status_code": resp.status_code,
                            "response_text": resp.text,
                        }
                    )
                    return HttpResponseRedirect(self.failure_url)

                self.request.session["user_profile"] = profile
                auth.login(self.request, self.user)

            else:
                logger.error(
                    "Accounts API returned error",
                    extra={
                        "username": self.user.username,
                        "status_code": resp.status_code,
                        "response_text": resp.text if resp.text else "<EMPTY_BODY>",
                        "response_bytes": resp.content if resp.content else b"<EMPTY_CONTENT>",
                        "headers": dict(resp.headers),
                        "url": getattr(resp.request, "url", "<UNKNOWN>"),
                        "method": getattr(resp.request, "method", "<UNKNOWN>"),
                    }
                )
                logger.error(f"RAW RESPONSE OBJECT: {resp!r}")
                logger.error(f"RAW REQUEST OBJECT: {resp.request!r}")
                
                return HttpResponseRedirect(self.failure_url)

        # Set id_token expiration (unchanged logic)
        expiration_interval = self.get_settings(
            "OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS", 60 * 15
        )
        self.request.session["oidc_id_token_expiration"] = (
            time.time() + expiration_interval
        )

        return HttpResponseRedirect(self.success_url)
