import requests, json, time
from django.conf import settings

class AASHEAccountsAPIClient:
    def __init__(self, accounts_base_url=None, accounts_api_key=None):
        self.accounts_base_url = accounts_base_url or settings.ACCOUNTS_BASE_URL
        self.accounts_api_key = accounts_api_key or settings.ACCOUNTS_API_KEY

        self.accounts_base_url = self.accounts_base_url + "/api/v1/"

        self.headers = { 
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {self.accounts_api_key}" 
        }

    def get_user_profile(self, username):

        response = requests.get(self.accounts_base_url + f"user_profile?username={username}", headers=self.headers)

        return response

class Auth0APIClient:
    def __init__(self, auth0_domain=None, auth0_client_id=None, auth0_client_secret=None):
        self.auth0_domain = auth0_domain or settings.AUTH0_DOMAIN
        self.auth0_client_id = auth0_client_id or settings.OIDC_RP_CLIENT_ID
        self.auth0_client_secret = auth0_client_secret or settings.OIDC_RP_CLIENT_SECRET

        self.auth0_base_url = f"https://{self.auth0_domain}/api/v2/"

        response = self.get_auth0_auth_token()
        if response["access_token"]:
            self.auth0_access_token = response["access_token"]
        else:
            print("Couldn't get API access: " + str(response))
            raise Exception("Couldn't get API access: " + str(response))

        self.headers = { 
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {self.auth0_access_token}" 
        }

    def get_auth0_auth_token(self):
        auth_url = "https://" + self.auth0_domain + "/oauth/token"

        payload = {
            "client_id": self.auth0_client_id,
            "client_secret": self.auth0_client_secret,
            "audience": "https://" + self.auth0_domain + "/api/v2/",
            "grant_type": "client_credentials"
        }

        headers = { 'content-type': "application/json" }

        response = requests.post(auth_url, json=payload, headers=headers)

        return json.loads(response.content)

    def create_organization(self, organization_slug, organization_name):

        payload = {
            "name": organization_slug,
            "display_name": organization_name,
        }

        response = requests.post(self.auth0_base_url + "organizations", json=payload, headers=self.headers)

        return response

    def delete_organization(self, organization_id):

        response = requests.delete(self.auth0_base_url + f"organizations/{organization_id}", headers=self.headers)

        return response

    def list_organizations(self, fetch_all=False, rate_limit_seconds=1):
        """ Fetches a list of 100 last created organizations, use fetch_all to get all. """

        orgs = []
        
        response = requests.get(self.auth0_base_url + "organizations?sort=created_at:-1&take=100", headers=self.headers)

        if response.status_code == 200:
            orgs.extend(response.json()["organizations"])
            while "next" in response.json() and fetch_all:
                response = requests.get(self.auth0_base_url + "organizations?sort=created_at:-1&take=100&from=" + response.json()["next"], headers=self.headers)
                orgs.extend(response.json()["organizations"])
        else:
            print("Couldn't get list of organizations: " + str(response))

        time.sleep(rate_limit_seconds)

        return orgs

    def update_organization(self, organization_id, metadata):

        response = requests.patch(self.auth0_base_url + f"organizations/{organization_id}", json={"metadata": metadata}, headers=self.headers) 

        return response

    def get_user_organizations(self, user_id):

        response = requests.get(self.auth0_base_url + f"users/{user_id}/organizations", headers=self.headers)

        return response

    def add_user_to_organization(self, user_id, organization_id):

        response = requests.post(self.auth0_base_url + f"organizations/{organization_id}/members", json={"members": [user_id,]}, headers=self.headers) 

        return response

    def get_active_users_count(self):

        response = requests.get(self.auth0_base_url + f"stats/active-users", headers=self.headers)

        return response

    def get_daily_stats(self):

        response = requests.get(self.auth0_base_url + f"stats/daily", headers=self.headers)

        return response

    def get_user(self, user_id):
        user_id = user_id.replace("_", "|") # revert to auth0 format

        response = requests.get(self.auth0_base_url + f"users/{user_id}", headers=self.headers)

        return response
