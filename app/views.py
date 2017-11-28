from django.shortcuts import render, get_object_or_404
from .models import *


def index(request):
    tags = Tag.objects.all()
    return render(request, 'index.html', {'tags': tags})


def rso(request, tag_id):
    organizations = Organization.objects.filter(tags=tag_id)
    return render(request, 'rsos.html', {'organizations': organizations})


def detail(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)
    return render(request, 'detail.html', {'organization': organization})

