"""tommy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

from crm.urls import (company as company_urls, contact as contact_urls,
                      job as job_urls, skill as skill_urls,
                      to_do as to_do_urls)
from user import urls as user_urls

urlpatterns = [
    url(
        r'^$',
        RedirectView.as_view(
            pattern_name='crm_company_list',
            permanent=False,
        ), name='takis'
    ),
    url(r'^admin/', admin.site.urls),
    url(r'^companies/', include(company_urls)),
    url(r'^contacts/', include(contact_urls)),
    url(r'^jobs/', include(job_urls)),
    url(r'^skills/', include(skill_urls)),
    url(r'^to-do-list/', include(to_do_urls)),
    url(r'^user/', include(user_urls, app_name='user', namespace='dj-auth')),
]


admin.site.site_header = 'Tommy'
