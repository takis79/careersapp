from django.conf.urls import url

from ..views import SkillCreate, SkillDetail, SkillList


urlpatterns = [
    url(
        r'^$',
        SkillList.as_view(),
        name='crm_skill_list'
    ),
    url(
        r'^create/$',
        SkillCreate.as_view(),
        name='crm_skill_create'
    ),
    url(
        r'^(?P<slug>[\w\-]+)/$',
        SkillDetail.as_view(),
        name='crm_skill_detail'
    ),
]