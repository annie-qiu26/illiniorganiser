# Reads tags.txt to create tags.
# tags.txt can define multiple parents for each tag. A parent
# is simply a prerequisite for a tag. For example,
# Academic is a parent of Chemistry because
# all chemistry clubs are academic.

from app.models import *


RESET_PARENTS = True  # delete all parent relations before starting
RESET_EVERYTHING = True  # delete all existing tags before starting


# add tags
with open('app/scripts/tags.txt') as tags_file:

    if RESET_EVERYTHING:
        Tag.objects.all().delete()
        print('Deleted all tags')

    breadth = 'B'

    for line in tags_file:
        line = line.replace('\n', '')
        if not line:
            pass
        elif line == 'Broad:':
            breadth = 'B'
        elif line == 'Specific:':
            breadth = 'S'
        elif line == 'Niche:':
            breadth = 'N'
        else:
            arr = line.split(' < ')
            tag = arr[0]
            obj, created = Tag.objects.get_or_create(name=tag, breadth=breadth)
            if created:
                print('Added', breadth, 'tag:', obj)


# add parents
with open('app/scripts/tags.txt') as tags_file:

    if RESET_PARENTS:
        for tag in Tag.objects.all():
            tag.parents.clear()
        print('Removed all parents')

    for line in tags_file:
        if '<' in line:
            line = line.replace('\n', '')
            arr = line.split(' < ')
            tag = Tag.objects.get(name__iexact=arr[0])
            parent_strings = arr[1].split(', ')

            for parent_string in parent_strings:
                parent = Tag.objects.get(name__iexact=parent_string)
                # print(parent.__dict__)
                tag.parents.add(parent)
                print('Added', parent, 'as parent to', tag)