from django.conf.urls import url


from ..views import (ContactCreate, ContactCreateGeneral, ContactDelete,
                     ContactDetail, ContactList, ContactUpdate)


urlpatterns = [
    url(
        r'^$',
        ContactList.as_view(),
        name='crm_contact_list'
    ),
    url(
        r'^create/$',
        ContactCreateGeneral.as_view(),
        name='crm_contact_create_general'
    ),
    url(
        r'^(?P<company_slug>[\w\-]+)/'
        r'add-contact/',
        ContactCreate.as_view(),
        name='crm_contact_create'
    ),
    url(
        r'^(?P<company_slug>[\w\-]+)/'
        r'(?P<contact_slug>[\w\-]+)/$',
        ContactDetail.as_view(),
        name='crm_contact_detail'
    ),
    url(
        r'^(?P<company_slug>[\w\-]+)/'
        r'(?P<contact_slug>[\w\-]+)/delete/$',
        ContactDelete.as_view(),
        name='crm_contact_delete'
    ),
    url(
        r'^(?P<company_slug>[\w\-]+)/'
        r'(?P<contact_slug>[\w\-]+)/update/$',
        ContactUpdate.as_view(),
        name='crm_contact_update'
    ),
]