from ninja import NinjaAPI
from django.core.management import call_command


api = NinjaAPI(urls_namespace="auth0_auth-api")

@api.get("/init-groups")
def add(request):
    
    try:
        call_command('my_command', 'foo', bar='baz')
    except Exception as e:
        return {
            "result": str(e)
        }

    return {
        "result": "OK"
    }
