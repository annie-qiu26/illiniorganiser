# Must be run after define_tags.py and download_orgs.py
#
# Uses natural language processing to automatically
# assign tags to organizations based on their
# names, summaries, and descriptions.

from rake_nltk import Rake
from app.models import Organization, Tag
import pprint


MIN_RELEVANCE = 2  # minimum RAKE relevance score for a keyword to be considered
DRY_RUN = False  # dry runs print would-be changes without saving them
VERBOSE = True  # print all candidate keywords with scores
RESET = True  # remove existing associations with tags before starting


r = Rake()
pp = pprint.PrettyPrinter()

orgs = list(Organization.objects.all())
tags = list(Tag.objects.all())

for org in orgs:

    text = "{}. {}. {} {}".format(org.name, org.category_name, org.summary, org.description)
    r.extract_keywords_from_text(text)

    print(org.name)
    print('-' * len(org.name))

    if RESET:
        if not DRY_RUN:
            org.tags.clear()
        print('Removed all tags')

    keywords_with_scores = r.get_ranked_phrases_with_scores()
    if VERBOSE:
        pp.pprint(keywords_with_scores)
    keywords_string = ' '.join([item[1] for item in
                                filter(lambda a: a[0] >= MIN_RELEVANCE, keywords_with_scores)])

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

    print('')
