from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.http import JsonResponse

from .models import *


def index(request):
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


def tag(request, tag_id):
    organizations = Organization.objects.filter(tags=tag_id)
    tag_obj = Tag.objects.get(id=tag_id)
    return render(request, 'app/rsos.html', {'organizations': organizations, 'tag': tag_obj})


def detail(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)
    positions = organization.organizationposition_set.all()
    return render(request, 'app/detail.html', {'organization': organization,
                                               'tags': organization.tags.all(),
                                               'users': {p.name: p.holders.all() for p in positions}
                                               })


def search_suggest(request):
    query = request.GET.get('q')
    tags = Tag.objects.filter(name__icontains=query).values('id', 'name')[:4]
    orgs = Organization.objects.filter(Q(name__icontains=query) | Q(abbr__icontains=query)).values('id', 'name', 'abbr')[:4]
    return JsonResponse({'results': [
                                     {'text': 'Organizations',
                                      'children': [{'type': 'org',
                                                    'id': org['id'],
                                                    'text': '{} ({})'.format(org['name'], org['abbr'])} for org in orgs]
                                      },
                                      {'text': 'Tags',
                                       'children': [{'type': 'tag',
                                                     'id': t['id'],
                                                     'text': t['name']} for t in tags]
                                       }
                                    ]})

