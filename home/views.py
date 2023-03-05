from django.http import JsonResponse
import json

def get_all_logs(request):
    res = {
        "success": True,
        "message": "Function based view: api to get logs"
    }
    return JsonResponse(res)

