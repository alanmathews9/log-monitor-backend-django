
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
def handle_logs(request, log_id):
    if request.method == 'POST':
        email_id = request.POST.get('email_id')
        log_item = log.objects.filter(id=log_id).first()
        if log_item is not None:
            log_item.handled_by = email_id if email_id is not None else ''
            log_item.handled_time = datetime.datetime.now()
            log_item.save()
            response_data = {'status': 'success', 'handled_by': log_item.handled_by, 'handled_time': log_item.handled_time.isoformat()}
            return HttpResponse(json.dumps(response_data), content_type='application/json')
    response_data = {'status': 'failure'}
    return HttpResponse(json.dumps(response_data), content_type='application/json')
