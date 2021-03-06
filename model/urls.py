from django.conf.urls import url
from . import views

import time,json

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<username>[-A-Za-z0-9]+)/models/$', views.models, name='models'),
    url(r'^(?P<username>[-A-Za-z0-9]+)/model/save/$', views.model_save, name='save'),
    url(r'^model/(?P<model_id>[-A-Za-z0-9]+)/$', views.model_get, name='get'),
    url(r'^model/(?P<model_id>[-A-Za-z0-9]+)/delete/$', views.model_delete, name='delete'),
    #url(r'^model/(?P<model_id>[-A-Za-z0-9]+)/run/$', views.model_run, name='run'),
    url(r'^model/(?P<model_id>[-A-Za-z0-9]+)/plan/$', views.model_plan, name='plan'),
    url(r'^model/(?P<model_id>[-A-Za-z0-9]+)/tasks/$', views.model_tasks, name='tasks'),


    url(r'^tasks/$', views.tasks, name='tasks'),
    url(r'^task/create/$', views.task_create, name='create_task'),
    #url(r'^task/create/(?P<model_id>[-A-Za-z0-9]+)/$', views.task_create, name='create_task'),
    url(r'^task/(?P<task_id>[-A-Za-z0-9]+)/state/$', views.task_state, name='state'),
    url(r'^task/(?P<task_id>[-A-Za-z0-9]+)/run/$', views.task_run, name='run'),
    url(r'^task/(?P<task_id>[-A-Za-z0-9]+)/stop/$', views.task_stop, name='stop'),
    url(r'^task/(?P<task_id>[-A-Za-z0-9]+)/download/(?P<node_id>[-A-Za-z0-9]+)/$', views.task_download, name='download'),

    #url(r'^model/(?P<model_id>[0-9]+)/$', views.model_get, name='get'),
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^register/$', views.user_register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^(?P<username>[-A-Za-z0-9]+)/logout/$', views.user_logout, name='logout'),
    url(r'^users/$', views.user_list, name='users'),
    url(r'^user/(?P<user_id>[-A-Za-z0-9]+)/delete/$', views.user_delete, name='user_delete'),
]