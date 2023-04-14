
from django.http import HttpResponse
import json
from .models import log
from django.views.decorators.csrf import csrf_exempt
import datetime

@csrf_exempt
def get_all_logs(request):
    response_data = { "logs": list(log.objects.values().all()) }
    return HttpResponse(json.dumps(response_data, default=str), content_type="application/json")

@csrf_exempt
def handle_log(request, log_id):
    current_user = request.user.email
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        l = log.objects.get(id=log_id)
        l.handled_by = current_user
        l.handled_time = current_time
        l.save()
        response_data = { "status": "success" }
    except log.DoesNotExist:
        response_data = { "status": "error", "message": "Log entry not found" }
    return HttpResponse(json.dumps(response_data), content_type="application/json")