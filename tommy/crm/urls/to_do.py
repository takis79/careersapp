from django.conf.urls import url

from ..views import CompanyActionToDoList


urlpatterns = [
    url(
        r'^$',
        CompanyActionToDoList.as_view(),
        name='crm_company_action_to_do_list'
    ),
]