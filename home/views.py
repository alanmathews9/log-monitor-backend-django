
from django.http import JsonResponse
from .models import log
from .models import user
def get_all_logs(request):
    logs = log.objects.all().values()  
    logs_list = list(logs)  
    return JsonResponse(logs_list,safe=False)



