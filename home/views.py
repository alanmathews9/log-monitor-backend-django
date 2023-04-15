
from django.http import HttpResponse
import json
from .models import log
from django.views.decorators.csrf import csrf_exempt
import datetime 
from basic_auth.userstore import get_email 

@csrf_exempt
def get_all_logs(request):
    response_data = { "logs": list(log.objects.values().all()) }
    return HttpResponse(json.dumps(response_data, default=str), content_type="application/json")

@csrf_exempt
def handle_log(request):
    if 'log_id' not in request.data:
        return HttpResponse(json.dumps({"type": "HandleLogResponse", "status": "failure", "reason": "log_id not present" }, default=str),
                            content_type="application/json")
    if 'comment' not in request.data:
        return HttpResponse(json.dumps({"type": "HandleLogResponse", "status": "failure", "reason": "comment not present" }, default=str),
                            content_type="application/json")
    log_id= request.data['log_id']
    comment = request.data['comment']
    handled_by = request.User.email
    handled_time = datetime.datetime.now()
    update_log = log.objects.filter(id=log_id).update(handled_by=handled_by, handled_time=handled_time, comment=comment)
    if update_log:
        return HttpResponse(json.dumps({"type": "HandleLogResponse", "status": "success" }, default=str),
                            content_type="application/json")
    
