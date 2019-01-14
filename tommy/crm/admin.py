from django.contrib import admin
from django.db.models import Count

from .models import (
    City, Company, CompanyAction, Contact, Country, Industry,
    Job, JobAction, Skill)


class CompanyAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(City)
admin.site.register(CompanyAction)
admin.site.register(Contact)
admin.site.register(Country)
admin.site.register(Industry)
admin.site.register(Job)
admin.site.register(JobAction)
admin.site.register(Skill)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    # List View
    list_display = ('name', 'city', 'get_assigned_to', 'job_count')
    list_filter = ('assigned_to', 'status')
    search_fields = ('name',)
    filter_horizontal = ('skills',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(job_number=Count('jobs'))

    def job_count(self, company):
        return company.job_number
    job_count.short_description = 'Open Jobs'
    job_count.admin_order_field = 'job_number'

    def get_assigned_to(self, company):
        return company.assigned_to.get_full_name()
    get_assigned_to.short_description = 'Assigned To'
    get_assigned_to.admin_order_field = 'assigned_to__first_name'
