# adds images to organizations from illiniorganizer-pictures
# pictures folder must be in same folder as this project

from PIL import Image
from os import listdir
from os.path import join, isdir, pardir
from termcolor import cprint

from django.db.models import Q
from django.core.files import File

from app.models import Tag, Organization, OrganizationPhoto


DRY_RUN = False  # dry runs print would-be changes without saving them
RESET = True

BASE_PATH = join(pardir, 'illiniorganizer-pictures')
TAGS_PATH = join(BASE_PATH, 'tag-photos')
ORGS_PATH = join(BASE_PATH, 'organization-photos')

# adds images to tags

for file_name in listdir(TAGS_PATH):
    print(join(TAGS_PATH, file_name))
    query = file_name.split('.')[0].replace('-', ' ')
    if query:
        try:
            tag = Tag.objects.get(name__iexact=query)
            if not DRY_RUN:
                tag.image.save(file_name, File(open(join(TAGS_PATH, file_name), 'rb')))
            cprint('Saved tag photo: {}'.format(file_name), 'green')
        except Tag.DoesNotExist:
            cprint('No tag contains query: {}'.format(query), 'red')


# adds images to organizations

if RESET:
    OrganizationPhoto.objects.all().delete()
    print('Deleted all organization photos')

for category_dir in [d for d in listdir(ORGS_PATH) if isdir(join(ORGS_PATH, d))]:
    for org_dir in [e for e in listdir(join(ORGS_PATH, category_dir)) if isdir(join(ORGS_PATH, category_dir, e))]:
        print(join(ORGS_PATH, category_dir, org_dir))
        query = org_dir.replace('-', ' ').replace('_', ' ')
        try:
            org = Organization.objects.get(Q(name__icontains=query) | Q(abbr__icontains=query))
            if OrganizationPhoto.objects.filter(organization=org).exists():
                print('Organization already has photos: {}'.format(org))
            else:
                for file_name in listdir(join(ORGS_PATH, category_dir, org_dir)):
                    if 'logo' in file_name:
                        if not DRY_RUN:
                            org.logo.save(file_name, File(open(join(ORGS_PATH, category_dir, org_dir, file_name), 'rb')))
                            cprint('Saved logo: {}'.format(file_name), 'green')
                    else:
                        img = OrganizationPhoto(organization=org, is_cover=('cover' in file_name or 'group' in file_name))
                        if not DRY_RUN:
                            img.image.save(file_name, File(open(join(ORGS_PATH, category_dir, org_dir, file_name), 'rb')))
                        cprint('Saved photo: {}'.format(file_name), 'green')
        except Organization.DoesNotExist:
            cprint('No organization contains query: {}'.format(query), 'red')
        except Organization.MultipleObjectsReturned:
            print('Multiple objects returned for query: {}'.format(query), 'red')


# img = Image.open(BASE_PATH + 'accounting-club/accounting-club-cover.jpg')
# print(img)