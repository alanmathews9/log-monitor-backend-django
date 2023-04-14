
from django.http import HttpResponse
import json
from .models import log
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def get_all_logs(request):
    response_data = { "logs": list(log.objects.values().all()) }
    return HttpResponse(json.dumps(response_data, default=str), content_type="application/json")


