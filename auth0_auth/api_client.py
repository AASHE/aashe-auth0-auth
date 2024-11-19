import requests, json, time
from django.conf import settings

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

    def list_organizations(self, rate_limit_seconds=0):
        orgs = []
        
        response = requests.get(self.auth0_base_url + "organizations?take=100", headers=self.headers)

        if response.status_code == 200:
            orgs.extend(response.json()["organizations"])
            while "next" in response.json():
                response = requests.get(self.auth0_base_url + "organizations?take=100&from=" + response.json()["next"], headers=self.headers)
                orgs.extend(response.json()["organizations"])
        else:
            print("Couldn't get list of organizations: " + str(response))

        time.sleep(rate_limit_seconds)

        return orgs

    def update_organization(self, organization_id, metadata):

        response = requests.patch(self.auth0_base_url + f"organizations/{organization_id}", json={"metadata": metadata}, headers=self.headers) 

        return response
