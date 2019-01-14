from django.conf.urls import url


from ..views import (CompanyCreate, CompanyDelete,
                     CompanyDetail, CompanyList, CompanyUpdate,
                     CompanyActionCreate, CompanyActionUpdate)

urlpatterns = [

    #################
    # COMPANY
    #################
    url(
        r'^$',
        CompanyList.as_view(),
        name='crm_company_list'
    ),
    url(
        r'^create/$',
        CompanyCreate.as_view(),
        name='crm_company_create'
    ),
    url(
        r'^(?P<slug>[\w\-]+)/$',
        CompanyDetail.as_view(),
        name='crm_company_detail'
    ),
    url(
        r'^(?P<slug>[\w\-]+)/delete/$',
        CompanyDelete.as_view(),
        name='crm_company_delete'
    ),
    url(
        r'^(?P<slug>[\w\-]+)/update/$',
        CompanyUpdate.as_view(),
        name='crm_company_update'
    ),

    ##################
    # COMPANY ACTION
    ##################
    url(
        r'^(?P<company_slug>[\w\-]+)/'
        r'add-action/$',
        CompanyActionCreate.as_view(),
        name='crm_company_action_create'
    ),
    url(
        r'^action/(?P<pk>\d+)/update/$',
        CompanyActionUpdate.as_view(),
        name='crm_company_action_update'
    ),
]