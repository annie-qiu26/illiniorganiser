from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import *


def index(request):
    queryset_list = Organization.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(Q(name__contains=query) |
                                             Q(abbr__contains=query) |
                                             Q(tags__name__contains=query)).distinct()

    context = {'tags': Tag.objects.filter(breadth='B')[:8],
               'organizations': [
                   {'name': 'Academic',
                    'orgs': Organization.objects.filter(tags__name='Academic')
                            .annotate(num_photos=Count('organizationphoto'))
                            .order_by('-num_photos')[:9],
                    },
                   {'name': 'Fun',
                    'orgs': Organization.objects.filter(tags__name='Fun')
                            .annotate(num_photos=Count('organizationphoto'))
                            .order_by('-num_photos')[:9]
                       ,
                    },
                   {'name': 'Greek Life',
                    'orgs': Organization.objects.filter(tags__name='Greek Life')
                            .annotate(num_photos=Count('organizationphoto'))
                            .order_by('-num_photos')[:9]
                       ,
                    },
                   {'name': 'Sports',
                    'orgs': Organization.objects.filter(tags__name='Sports')
                            .annotate(num_photos=Count('organizationphoto'))
                            .order_by('-num_photos')[:9]
                       ,
                    }
               ]
               }

    return render(request, 'app/index.html', context)


def rso(request, tag_id):
    organizations = Organization.objects.filter(tags=tag_id)
    return render(request, 'app/rsos.html', {'organizations': organizations})


def detail(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)
    positions = organization.organizationposition_set.all()
    print({p.name: p.holders.all() for p in positions})
    return render(request, 'app/detail.html', {'organization': organization,
                                               'tags': organization.tags.all(),
                                               'users': {p.name: p.holders.all() for p in positions}
                                               })

