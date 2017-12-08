from __future__ import unicode_literals

from django.db import models

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

from django.contrib.auth.models import User


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    claimed = models.BooleanField(
        _('claimed'),
        default=True,
        help_text=_('Designates whether a real person has claimed this account.')
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def __str__(self):              # __unicode__ on Python 2
        return self.email


class Tag(models.Model):
    TAG_BREADTHS = (
        ('B', 'BROAD'),
        ('S', 'SPECIFIC'),
        ('N', 'NICHE')
    )
    name = models.CharField(_('tag'), max_length=64, unique=True)
    breadth = models.CharField(_('breadth'), max_length=1, choices=TAG_BREADTHS, default='N')
    parents = models.ManyToManyField('self', blank=True, symmetrical=False)
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
    tags = models.ManyToManyField(Tag)
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
        verbose_name = _('organization positions')
        verbose_name_plural = _('organization positions')
        ordering = ['name']