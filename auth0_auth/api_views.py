from ninja import NinjaAPI
from django.core.management import call_command


api = NinjaAPI(urls_namespace="auth0_auth-api")

@api.post("/init-groups")
def init_groups(request):
    
    try:
        call_command('init_groups')
    except Exception as e:
        return {
            "result": str(e)
        }

    return {
        "result": "OK"
    }
