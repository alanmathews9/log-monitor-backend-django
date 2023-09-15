
from django.http import HttpResponse
import json
from .models import log
# from basic_auth.models import User
from django.views.decorators.csrf import csrf_exempt
import datetime 
from basic_auth.userstore import User
from home.log_reader import start_all_log_reader_threads
from mysite.settings import LOG_MONITOR_ROOT_DIR as root_dir
start_all_log_reader_threads(root_dir)  # this will start all the log reader threads when the server starts


@csrf_exempt    # decorator used to exempt csrf token validation which is a protection against cross site request forgery
def get_all_logs(request):
    response_data = { "logs": list(log.objects.values().all()) }    # dictionary with key as "logs" and value as list of all logs
    # json.dumps is used to serialize the data into json formatted string
    return HttpResponse(json.dumps(response_data, default=str), content_type="application/json")   

@csrf_exempt
def handle_log(request):
    if 'log_id' not in request.data:
        return HttpResponse(json.dumps({"type": "HandleLogResponse", "status": "failure", "reason": "log_id not present" }, default=str),
                            content_type="application/json")
    if 'comment' not in request.data:
        return HttpResponse(json.dumps({"type": "HandleLogResponse", "status": "failure", "reason": "comment not present" }, default=str),
                            content_type="application/json")
    # if you get the log_id and comment, then update the log table with handled_by, handled_time and comment
    log_id= request.data['log_id']
    comment = request.data['comment']
    handled_by = request.user.get_email()   # get_email() is a method in User class
    handled_time = datetime.datetime.now()
    update_log = log.objects.filter(id=log_id).update(handled_by=handled_by, handled_time=handled_time, comment=comment)
    
    if update_log:  # if the update was successful
        return HttpResponse(json.dumps({"type": "HandleLogResponse", "status": "success" }, default=str),
                            content_type="application/json")
    
