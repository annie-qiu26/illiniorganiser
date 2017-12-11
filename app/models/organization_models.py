from __future__ import unicode_literals

from django.db import models

from django.utils.translation import ugettext_lazy as _


class Tag(models.Model):
    TAG_BREADTHS = (
        ('B', 'BROAD'),
        ('S', 'SPECIFIC'),
        ('N', 'NICHE')
    )
    name = models.CharField(_('tag'), max_length=64, unique=True)
    breadth = models.CharField(_('breadth'), max_length=1, choices=TAG_BREADTHS, default='N')
    parents = models.ManyToManyField('self', blank=True, symmetrical=False)
    image = models.ImageField(_('image'), null=True, blank=True)
    # organizationCount = models.IntegerField(_('Organization Count'), default=0)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['name']


class Organization(models.Model):
    tags = models.ManyToManyField(Tag, blank=True)
    name = models.CharField(_('name'), max_length=64, unique=True)
    abbr = models.CharField(_('abbreviation'), max_length=10, null=True, blank=True, default='')
    found_date = models.DateTimeField(_('date founded'))
    end_date = models.DateTimeField(_('date ended'), null=True, blank=True)
    summary = models.TextField(_('summary'), max_length=256, default='')
    description = models.TextField(_('description'), default='')
    logo = models.ImageField(_('logo'), blank=True, null=True)
    members = models.IntegerField(_('number of members'), default=0)
    email = models.EmailField(_('organization email'), null=True, blank=True)
    is_public = models.BooleanField(_('is public'), default=False)
    last_modified = models.DateTimeField(_('last modified'), null=True, blank=True, auto_now_add=True)
    is_deleted = models.BooleanField(_('deleted'), default=False)
    category_name = models.CharField(_('category name'), max_length=64, blank=True)
    website_url = models.URLField(_('website url'), null=True, blank=True)

    def get_cover(self):
        try:
            return OrganizationPhoto.objects.get(organization=self, is_cover=True)
        except OrganizationPhoto.DoesNotExist:
            return None

    def __str__(self):
        return self.name + (" (" + self.abbr + ")" if self.abbr else "")

    def __unicode__(self):
        return self.name + (" (" + self.abbr + ")" if self.abbr else "")

    class Meta:
        verbose_name = _('RSO')
        verbose_name_plural = _('RSOs')
        ordering = ['name']
        unique_together = ['name', 'abbr']


class OrganizationPosition(models.Model):
    POSITION_TYPES = (
        ('F', 'FACULTY'),
        ('A', 'ADMIN'),
        ('M', 'MODERATOR')
    )
    name = models.CharField(_('name'), max_length=64)
    type = models.CharField(_('position type'), max_length=1, choices=POSITION_TYPES, default='M')
    description = models.CharField(_('position description'), max_length=256, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    holders = models.ManyToManyField('MyUser', blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('organization position')
        verbose_name_plural = _('organization positions')
        ordering = ['name']


class OrganizationPhoto(models.Model):
    image = models.ImageField(_('image'))
    caption = models.CharField(_('caption'), max_length=128, blank=True, null=True)
    is_cover = models.BooleanField(_('is cover photo'), default=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.image.name

    def __unicode__(self):
        return self.image.name

    class Meta:
        verbose_name = _('organization photo')
        verbose_name_plural = _('organization photos')
        ordering = ['is_cover']