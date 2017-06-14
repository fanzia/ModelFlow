from django.shortcuts import render
from django.http import HttpResponse

from . import models
from .models import Model, Task
from .Graph import Graph
import ModelFlow

from django.utils import timezone

import time, json, uuid, datetime, os, os.path

# Create your views here.

def index(request):
    return HttpResponse("hello world.")

def model_save(request):

    text = request.body.decode('utf-8')
    create_time = timezone.now()
    obj = json.loads(text)
    obj["create_time"] = str(create_time)
    name = obj["name"]

    #生成Model
    model = Model(
        name=name,
        description=name,
        create_time=create_time,
        text=json.dumps(obj))
    model.save();

    #创建model目录(不要了)
    # model_folder = os.path.join(
    #     os.path.join(
    #         os.path.join(
    #             os.path.join(ModelFlow.settings.BASE_DIR, "static"),
    #             "data"
    #         ),
    #         "model",
    #     ),
    #     str(model.uuid)
    # )
    #os.mkdir(model_path)

    return HttpResponse(model.uuid)

"""
返回所有的Model
"""
def models(request):

    obj = []
    models = Model.objects.all()
    for model in models:
        obj.append(model.exportToJson())

    return HttpResponse(json.dumps(obj), content_type="application/json")

"""
返回指定id的Model
"""
def model_get(request, model_id):
    try:
        model = Model.objects.get(uuid=model_id)
    except Model.DoesNotExist:
        raise Http404("Model does not exist")
    return HttpResponse(model.text, content_type="application/json")

def model_plan(request, model_id):
    model = Model.objects.filter(uuid=model_id)[0]
    graph = Graph()
    if not graph.load(model.text):
        return HttpResponse("Error")
    else:
        flow = graph.plan()
        plan = ""
        for s in flow:
            plan += "{0}({1})-->".format(s.getID(), s.getName())
        return HttpResponse(plan)

"""
获取model_id指定的Model下面的Task
"""
def model_tasks(request, model_id):
    try:
        models = Model.objects.filter(uuid=model_id)

        if len(models) == 0:
            return HttpResponse("no model [{0}]".format(model_id))

        model = models[0]
        tasks = model.task_set.all()

        obj = []
        for task in tasks:
            obj.append(task.exportToJson())
        text = json.dumps(obj)
        return HttpResponse(text, content_type="application/json")
    except:
        return HttpResponse("Error")


"""
获取Task的状态
"""
def tasks(request):

    tasks = Task.objects.all()

    obj = []
    for task in tasks:
        obj.append(task.exportToJson())
    text = json.dumps(obj)
    return HttpResponse(text, content_type="application/json")

"""
获取指定Task的状态
"""
def task_state(request, task_id):
    try:
        tasks = Task.objects.filter(uuid=task_id)

        if len(tasks) == 0:
            return HttpResponse("no task [{0}]".format(model_id))

        task = tasks[0]
    except:
        return HttpResponse("Error")

    processes = task.process_set.all()

    obj = {
        "id": task.id,
        "name": task.name,
        "uuid": str(task.uuid),
        "model": str(task.model_id),
        "state": task.state,
        "start_time": str(task.start_time),
        "end_time": str(task.end_time),
        "processes" : []
    }

    for process in processes:
        obj["processes"].append(process.exportToJson())
    text = json.dumps(obj)
    return HttpResponse(text, content_type="application/json")


"""
启动模型计算
返回Task的uuid
"""
def model_run(request, model_id):

    try:
        models = Model.objects.filter(uuid=model_id)
    except:
        return HttpResponse("Error")

    if not models:
        return HttpResponse("Error")

    str1 = start_task(model_id)

    #return HttpResponse("{0}".format(task.uuid))
    return HttpResponse(str1)



"""
启动模型计算
"""
def start_task(model_id):
    model = Model.objects.filter(uuid=model_id)[0]

    graph = Graph()
    if not graph.load(model.text):
        pass
    else:
        #创建task
        task = model.task_set.create(
            uuid=uuid.uuid4(),
            name=model.name,
            start_time=timezone.now(),
            end_time=timezone.now(),
        )
        task.state = 1
        task.save()

        #生成执行计划
        flow = graph.plan()
        if flow:
            #生成执行步骤及其状态,记录Process的状态
            processes = []
            for func in flow:
                process = task.process_set.create(
                    name = func.getName(),
                    start_time = timezone.now(),
                    end_time = timezone.now()
                )
                process.save()
                processes.append(process)

            #执行Plan
            count = len(processes)
            for i in range(count):
                #执行func
                #更新process的状态为正在执行
                process = processes[i]
                process.state = 1
                process.save()

                #time.sleep(5)
                func = flow[i]
                #processing func

                #更新process的状态为结束，并记录结束时间
                process.end_time = timezone.now()
                process.state = 2
                process.save()
                pass

        task.state = 2
        task.save()
    return task.uuid