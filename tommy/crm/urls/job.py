from django.conf.urls import url

from ..views import (JobCreate, JobCreateGeneral, JobDelete, JobDetail,
                     JobList, JobActionCreate, JobUpdate)


urlpatterns = [
    url(
        r'^$',
        JobList.as_view(),
        name='crm_job_list'
    ),
    url(
        r'^create/$',
        JobCreateGeneral.as_view(),
        name='crm_job_create_general'
    ),
    url(
        r'^(?P<company_slug>[\w\-]+)/'
        r'add-job/$',
        JobCreate.as_view(),
        name='crm_job_create'
    ),
    url(
        r'^(?P<company_slug>[\w\-]+)/'
        r'(?P<job_slug>[\w\-]+)/$',
        JobDetail.as_view(),
        name='crm_job_detail'
    ),
    url(
        r'^(?P<company_slug>[\w\-]+)/'
        r'(?P<job_slug>[\w\-]+)/'
        r'delete/$',
        JobDelete.as_view(),
        name='crm_job_delete'
    ),
    url(
        r'^(?P<company_slug>[\w\-]+)/'
        r'(?P<job_slug>[\w\-]+)/'
        r'update/$',
        JobUpdate.as_view(),
        name='crm_job_update'
    ),
    url(
        r'^(?P<company_slug>[\w\-]+)/'
        r'(?P<job_slug>[\w\-]+)/'
        r'add-action/$',
        JobActionCreate.as_view(),
        name='crm_job_action_create'
    ),

]
