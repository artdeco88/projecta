from django.core.urlresolvers import reverse
from django.utils.text import slugify
import logging
logger = logging.getLogger(__name__)
from django.db import models
from audited_models.models import AuditedModel
from django.utils.translation import ugettext_lazy as _


class ApprovedCategoryManager(models.Manager):
    """Custom category manager that shows only approved records."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            ApprovedCategoryManager, self).get_query_set().filter(
                approved=True)


class UnapprovedCategoryManager(models.Manager):
    """Custom version manager that shows only unapproved records."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            UnapprovedCategoryManager, self).get_query_set().filter(
                approved=False)


class Category(AuditedModel):
    """A category model e.g. gui, backend, web site etc."""
    name = models.CharField(
        help_text=_('Name of this category.'),
        max_length=255,
        null=False,
        blank=False,
        unique=False)  # there is a unique together rule in meta class below

    approved = models.BooleanField(
        help_text=_(
            'Whether this version has been approved for use by the '
            'project owner.'),
        default=False
    )

    sort_number = models.SmallIntegerField(
        help_text=(
            'The order in which this category is listed within a '
            'project'),
        default=0
    )
    slug = models.SlugField(unique=True)
    project = models.ForeignKey('base.Project')
    objects = models.Manager()
    approved_objects = ApprovedCategoryManager()
    unapproved_objects = UnapprovedCategoryManager()

    class Meta:
        """Meta options for the category class."""
        unique_together = ('name', 'project')
        app_label = 'changes'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s : %s' % (self.project.name, self.name)

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={
            'slug': self.slug,
            'project_slug': self.project.slug
        })
