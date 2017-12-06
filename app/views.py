from django.shortcuts import render, get_object_or_404
from .models import *


def index(request):
    return render(request, 'app/index.html', {'tags': Tag.objects.filter(breadth='B')[:8],
                                              'academic_orgs': Organization.objects.filter(tags__name='Academic')[:4],
                                              'fun_orgs': Organization.objects.filter(tags__name='Fun')[:4],
                                              'greek_orgs': Organization.objects.filter(tags__name='Greek Life')[:4],
                                              'sports_orgs': Organization.objects.filter(tags__name='Sports')[:4]
                                              })


def rso(request, tag_id):
    organizations = Organization.objects.filter(tags=tag_id)
    return render(request, 'app/rsos.html', {'organizations': organizations})


def detail(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)
    return render(request, 'app/detail.html', {'organization': organization,
                                               'tags': organization.tags.all()})

