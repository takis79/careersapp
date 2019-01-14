from django.core.urlresolvers import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  ListView, UpdateView)

from user.decorators import class_login_required
from .forms import (CompanyForm, CompanyActionForm, CompanyActionUpdateForm,
                    ContactForm, ContactFormGeneral, JobForm, JobFormGeneral,
                    JobActionForm, SkillForm)
from .models import Company, CompanyAction, Contact, Job, JobAction, Skill
from .utils import (InjectCompanyContextMixin, InjectCompanyInitialMixin,
                    ContactGetObjectMixin, CreatedByFormValidMixin,
                    InjectJobContextMixin, InjectJobInitialMixin,
                    JobGetObjectMixin, PageLinksMixin)


@class_login_required
class CompanyCreate(CreatedByFormValidMixin, CreateView):
    form_class = CompanyForm
    model = Company

    def get_initial(self):
        from django.contrib.auth import get_user
        current_user = get_user(self.request)
        initial = {
            'owner': current_user,
            'assigned_to': current_user
        }
        initial.update(self.initial)
        return initial


@class_login_required
class CompanyDelete(DeleteView):
    model = Company
    success_url = reverse_lazy('crm_company_list')


@class_login_required
class CompanyDetail(DetailView):
    model = Company


@class_login_required
class CompanyList(PageLinksMixin, ListView):
    model = Company


@class_login_required
class CompanyUpdate(CreatedByFormValidMixin, UpdateView):
    form_class = CompanyForm
    model = Company
    template_name = 'crm/company_form_update.html'


@class_login_required
class CompanyActionToDoList(PageLinksMixin, ListView):
    queryset = CompanyAction.objects.filter(status='to_do')
    context_object_name = 'company_action_to_do_list'
    template_name = 'crm/company_action_to_do_list.html'


@class_login_required
class CompanyActionCreate(CreatedByFormValidMixin, InjectCompanyContextMixin,
                          InjectCompanyInitialMixin, CreateView):
    form_class = CompanyActionForm
    model = CompanyAction
    template_name = 'crm/company_action_form.html'


@class_login_required
class CompanyActionUpdate(UpdateView):
    form_class = CompanyActionUpdateForm
    model = CompanyAction
    context_object_name = 'company_action'
    template_name = 'crm/company_action_update.html'


@class_login_required
class ContactCreate(CreatedByFormValidMixin, InjectCompanyContextMixin,
                    InjectCompanyInitialMixin, CreateView):
    form_class = ContactForm
    model = Contact


@class_login_required
class ContactCreateGeneral(CreatedByFormValidMixin, CreateView):
    form_class = ContactFormGeneral
    model = Contact


@class_login_required
class ContactDelete(InjectCompanyContextMixin, ContactGetObjectMixin, DeleteView):
    model = Contact
    success_url = reverse_lazy('crm_contact_list')
    slug_url_kwarg = 'contact_slug'


@class_login_required
class ContactDetail(InjectCompanyContextMixin, ContactGetObjectMixin, DetailView):
    model = Contact
    slug_url_kwarg = 'contact_slug'


@class_login_required
class ContactList(PageLinksMixin, ListView):
    model = Contact


@class_login_required
class ContactUpdate(CreatedByFormValidMixin, InjectCompanyContextMixin,
                    ContactGetObjectMixin, UpdateView):
    form_class = ContactForm
    model = Contact
    template_name = 'crm/contact_form_update.html'
    slug_url_kwarg = 'contact_slug'


@class_login_required
class JobCreate(CreatedByFormValidMixin, InjectCompanyContextMixin,
                InjectCompanyInitialMixin, CreateView):
    form_class = JobForm
    model = Job


@class_login_required
class JobCreateGeneral(CreatedByFormValidMixin, CreateView):
    form_class = JobFormGeneral
    model = Job


@class_login_required
class JobDelete(InjectCompanyContextMixin, JobGetObjectMixin, DeleteView):
    model = Job
    success_url = reverse_lazy('crm_job_list')
    slug_url_kwarg = 'job_slug'


@class_login_required
class JobDetail(InjectCompanyContextMixin, JobGetObjectMixin, DetailView):
    model = Job
    slug_url_kwarg = 'job_slug'


@class_login_required
class JobList(PageLinksMixin, ListView):
    model = Job


@class_login_required
class JobUpdate(CreatedByFormValidMixin, InjectCompanyContextMixin,
                JobGetObjectMixin, UpdateView):
    form_class = JobForm
    model = Job
    template_name = 'crm/job_form_update.html'
    slug_url_kwarg = 'job_slug'


@class_login_required
class JobActionCreate(CreatedByFormValidMixin, InjectJobContextMixin,
                      InjectJobInitialMixin, CreateView):
    form_class = JobActionForm
    model = JobAction
    template_name = 'crm/job_action_form.html'


@class_login_required
class SkillCreate(CreateView):
    form_class = SkillForm
    model = Skill


@class_login_required
class SkillDetail(DetailView):
    model = Skill


@class_login_required
class SkillList(PageLinksMixin, ListView):
    model = Skill

