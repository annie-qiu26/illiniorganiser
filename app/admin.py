from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import *


# Register your models here.
admin.site.register(Tag)
admin.site.register(Organization)

