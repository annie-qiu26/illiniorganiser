from rake_nltk import Rake
from app.models import Organization, Tag
import pprint


TOLERANCE = 12  # number of keywords to consider
DRY_RUN = True  # dry runs print would-be changes without saving them
RESET = False  # remove existing associations with tags before starting


r = Rake()
pp = pprint.PrettyPrinter()

orgs = list(Organization.objects.all()[:50])
tags = list(Tag.objects.all())

for org in orgs:
    if RESET:
        org.tags.clear()
        print('Removed all tags')

    text = org.name + '. ' + org.summary + ' ' + org.description
    r.extract_keywords_from_text(text)

    print('')
    print(org.name)
    print('-' * len(org.name))

    keywords_string = ' '.join(r.get_ranked_phrases()[:TOLERANCE])

    for tag in tags:
        if tag.name.lower() in keywords_string:
            print('Assigned tag:', tag)
            org.tags.add(tag)
            parents = tag.parents.all()
            for parent in parents:
                org.tags.add(parent)
                print('Assigned tag:', parent, '- parent of:', tag)

    if not DRY_RUN:
        org.save()
