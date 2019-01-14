from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


def get_unique_slug(model, slug):
    """
    Simple implementation to generate unique slug fields.
    Args:
        model: Model to generate the slug for. Ex: Company, Job, etc.
        slug: slugified text, usually from model name or title
    Returns: unique slug for that model with correlative number at the end
    """
    original_slug = slug
    slug_count = model.objects.filter(slug__iexact=slug).count()

    if slug_count > 0:
        i = 0
        while True:
            i += 1
            slug = slug.rsplit('-', 1)[0]
            # If after splitting, we have the original slug, we can just add
            # the correlative number
            if slug == original_slug:
                slug = ('{}-{}'.format(slug, i))
            # If after splitting we don't have the original slug, we might
            # have split the slug itself, ex ['rodrigo', 'villatoro'].
            # In this case, we need to add correlative to original slug
            else:
                slug = ('{}-{}'.format(original_slug, i))
            if model.objects.filter(slug__iexact=slug).count() == 0:
                break
    return slug


class Industry(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'industries'

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=31, db_index=True, unique=True)
    slug = models.SlugField(max_length=31, unique=True)

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('crm_skill_detail', kwargs={'slug': self.slug})

    def clean(self):
        self.name = self.name.lower()

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            self.slug = get_unique_slug(Skill, slug)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name


class Country(models.Model):
    country_code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'countries'

    def __str__(self):
        return self.name


class City(models.Model):
    geonameid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    feature_code = models.CharField(max_length=15)
    country = models.ForeignKey(Country, related_name='cities')
    population = models.IntegerField(default=0)

    class Meta:
        ordering = ('name', 'country')
        verbose_name_plural = 'cities'

    def __str__(self):
        return '{}'.format(self.name)


class Company(models.Model):
    STATUS_CHOICES = (
        ('contacted', 'Contacted'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('n/a', 'N/A'),
    )
    name = models.CharField(max_length=100, db_index=True)
    legal_name = models.CharField(max_length=100, blank=True)
    cif = models.CharField(max_length=25, blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    official_company = models.BooleanField(
        default=True,
        help_text='Official company in Nubelo, in case of duplicates',
        blank=True)
    fee = models.CharField(max_length=25, blank=True)
    nubelo_id = models.IntegerField(null=True, blank=True)
    nubelo_url = models.URLField(max_length=250, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    city = models.ForeignKey(City, related_name='companies')
    industry = models.ForeignKey(Industry, related_name='companies')
    skills = models.ManyToManyField(Skill, related_name='companies')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='created_companies',
        db_index=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='owned_companies')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='assigned_companies')

    class Meta:
        ordering = ('-timestamp',)
        verbose_name_plural = "companies"

    def get_absolute_url(self):
        return reverse('crm_company_detail', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('crm_company_delete', kwargs={'slug': self.slug})

    def get_job_create_url(self):
        return reverse(
            'crm_job_create', kwargs={'company_slug': self.slug})

    def get_company_action_create_url(self):
        return reverse(
            'crm_company_action_create', kwargs={'company_slug': self.slug})

    def get_contact_create_url(self):
        return reverse(
            'crm_contact_create', kwargs={'company_slug': self.slug})

    def get_update_url(self):
        return reverse('crm_company_update', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            self.slug = get_unique_slug(Company, slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CompanyAction(models.Model):
    ACTION_CHOICES = (
        ('phone_call', 'Phone call'),
        ('meeting', 'Meeting'),
        ('email', 'Email'),
        ('proposal_sent', 'Proposal Sent'),
        ('proposal_signed', 'Proposal Signed'),
        ('blind_cv', 'Blind CV'),
        ('other', 'Other'),
    )
    STATUS_CHOICES = (
        ('to_do', 'To Do'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    status = models.CharField(
        max_length=25, choices=STATUS_CHOICES, default='to_do')
    description = models.TextField()
    blind_cvs_sent = models.IntegerField(default=0)
    is_highlighted = models.BooleanField(default=False)
    document = models.FileField(
        upload_to='uploads/actions/companies/%Y/%m/%d/', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    completed_timestamp = models.DateTimeField(null=True, db_index=True)
    company = models.ForeignKey(Company, related_name='company_actions')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='company_actions',
        db_index=True)

    class Meta:
        ordering = ('-timestamp',)

    def get_absolute_url(self):
        return self.company.get_absolute_url()

    def get_update_url(self):
        return reverse('crm_company_action_update', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.status == 'done':
            if not self.completed_timestamp:
                self.completed_timestamp = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.action


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, db_index=True)
    title = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=250, db_index=True)
    phone = models.CharField(max_length=25, blank=True)
    mobile = models.CharField(max_length=25, blank=True)
    address = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    is_primary_contact = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    company = models.ForeignKey(Company, related_name='contacts')
    city = models.ForeignKey(City, related_name='contacts')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='contacts',
        db_index=True)

    class Meta:
        ordering = ('-is_primary_contact',)

    def get_absolute_url(self):
        return reverse(
            'crm_contact_detail',
            kwargs={
                'company_slug': self.company.slug,
                'contact_slug': self.slug,
            })

    def get_delete_url(self):
        return reverse(
            'crm_contact_delete',
            kwargs={
                'company_slug': self.company.slug,
                'contact_slug': self.slug,
            })

    def get_update_url(self):
        return reverse(
            'crm_contact_update',
            kwargs={
                'company_slug': self.company.slug,
                'contact_slug': self.slug,
            })

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.get_full_name())
            self.slug = get_unique_slug(Contact, slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}: {}'.format(self.email, self.company)


class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('employee', 'Employee'),
        ('freelance', 'Freelance'),
    )
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('canceled_by_client', 'Canceled by Client'),
    )
    title = models.CharField(max_length=250, db_index=True)
    description = models.TextField()
    zip_code = models.CharField(max_length=10, blank=True)
    num_vacancies = models.IntegerField(default=1)
    job_type = models.CharField(max_length=15, choices=JOB_TYPE_CHOICES)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    fee = models.CharField(max_length=25, blank=True)
    total_income = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    document = models.FileField(
        upload_to='uploads/docs/jobs/%Y/%m/%d/', blank=True)
    slug = models.SlugField(max_length=250, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    nubelo_id = models.IntegerField(null=True, blank=True)
    nubelo_url = models.URLField(max_length=250, blank=True)
    company = models.ForeignKey(Company, related_name='jobs')
    skills = models.ManyToManyField(Skill, related_name='jobs')
    city = models.ForeignKey(City, related_name='jobs')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='created_jobs',
        db_index=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='assigned_jobs')

    class Meta:
        ordering = ('-timestamp',)

    def get_absolute_url(self):
        return reverse(
            'crm_job_detail',
            kwargs={
                'company_slug': self.company.slug,
                'job_slug': self.slug,
            })

    def get_delete_url(self):
        return reverse(
            'crm_job_delete',
            kwargs={
                'company_slug': self.company.slug,
                'job_slug': self.slug,
            })

    def get_job_action_create_url(self):
        return reverse(
            'crm_job_action_create',
            kwargs={
                'company_slug': self.company.slug,
                'job_slug': self.slug,
            })

    def get_update_url(self):
        return reverse(
            'crm_job_update',
            kwargs={
                'company_slug': self.company.slug,
                'job_slug': self.slug
            })

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            self.slug = get_unique_slug(Job, slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}: {}'.format(self.company, self.title)


class JobAction(models.Model):
    ACTION_CHOICES = (
        ('candidates_sent', 'Candidates Sent'),
        ('client_interviewed_candidate', 'Client Interviewed Candidate'),
        ('client_made_job_offer', 'Client Made Job Offer'),
        ('candidate_accepted_offer', 'Candidate Accepted Offer'),
        ('candidate_rejected_offer', 'Candidate Rejected Offer'),
        ('other', 'Other'),
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    action_num_candidates = models.IntegerField(default=1)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    is_highlighted = models.BooleanField(default=False)
    document = models.FileField(
        upload_to='uploads/actions/job/%Y/%m/%d/', blank=True)
    job = models.ForeignKey(Job, related_name='job_actions')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='job_actions',
        db_index=True)

    class Meta:
        ordering = ('-timestamp',)

    def get_absolute_url(self):
        return self.job.get_absolute_url()

    def __str__(self):
        return '{}: {}'.format(self.job, self.action)


# Reports
# Por usuario: número de llamadas, visitas, candidatos enviados, entrevistas, blind cv,
# BUSCADOR DE EMPRESAS: código postal, sector, skill, etc.
# Las notas no pueden editarse
# Sincronizar todas las empresas que esten en bbdd que no tengan mailinator.