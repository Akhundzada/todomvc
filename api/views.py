import json
from bson import json_util
from django.http import HttpResponse
from .models import Task


def index(request):
    task_list = Task.objects.filter(status__exact=1).values()
    return HttpResponse(json.dumps(list(task_list)))


def update(request):
    if request.method == 'POST':
        try:
            params = json.loads(request.body.decode('utf-8'))
        except ValueError:
            return HttpResponse([{'code': 500, 'message': 'Decode error'}])

        task_list = Task.objects.filter(status__exact=1)
        collected_task_ids = task_list.values_list('pk', flat=True)

        for task in task_list:
            for param in params:
                if param['id'] not in collected_task_ids:
                    task = Task(title=param['title'], completed=0, status=1)
                    task.save()
                    continue

                if param['id'] == task.pk:
                    task.title = param['title']
                    task.completed = param['completed']
                    task.save()
            return HttpResponse([{'code': 200, 'message': 'OK'}])
        else:
            return HttpResponse([{'code':500, 'message': 'No records found'}])

    return HttpResponse([{'code': 500, 'message': 'Request is not an AJAX or'
                                                  'POST or no data found'}])


def prepare_item(object):
    return {
        'id': object.pk,
        'title': object.name,
        'completed': object.is_completed,
        'created_at': object.created_at
    }



