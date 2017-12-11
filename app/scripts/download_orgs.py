# Reads organizations.json and downloads
# detailed organization data from U of I connections.


from urllib import request
from urllib.error import HTTPError
import json
import pprint
from app.models import Organization
import html2text


DRY_RUN = False  # dry runs print would-be changes without saving them
DOWNLOAD_ALL = False  # true for production, false for testing when you don't want to download everything
ORGS_RANGE = range(400, 450)  # if DOWNLOAD_ALL is false, only pull this range of organizations
VERBOSE = True  # print details of each organization
RESET = True  # delete all existing organizations before starting

pp = pprint.PrettyPrinter()
URL_BASE = 'https://illinois.campuslabs.com/engage/api/discovery/organization/bykey/'
with open('app/scripts/organizations.json', encoding='utf8') as file:

    if RESET:
        Organization.objects.all().delete()
        print('Deleted all organizations')

    organizations = json.load(file)

    for i in (range(len(organizations)) if DOWNLOAD_ALL else ORGS_RANGE):
        org_brief_data = organizations['value'][i]

        if Organization.objects.filter(name=org_brief_data['Name']).exists():
            print('Already exists: {}'.format(org_brief_data['Name']))
        else:
            print('Downloading...: {}'.format(org_brief_data['Name']))
            try:
                response = request.urlopen(URL_BASE + org_brief_data['WebsiteKey'])
            except HTTPError:
                print('Could not download: {}'.format(org_brief_data['Name']))
                continue

            org_data = json.loads(response.read().decode())

            if VERBOSE:
                pp.pprint(org_data)
            else:
                print('Successfully downloaded: {}'.format(org_data['name']))

            org_object = Organization(name=org_data['name'],
                                      abbr=(org_data['shortName'] if org_data['shortName'] else None),
                                      found_date=org_data['startDate'],
                                      summary=org_data['summary'],
                                      description=html2text.html2text(org_data['description']) if org_data['description'] else org_data['summary'],
                                      is_public=True,
                                      email=org_data['email'],
                                      last_modified=org_data['modifiedOn'],
                                      is_deleted=org_data['deleted'],
                                      category_name=org_brief_data['CategoryNames'][0]
                                      )
            if not DRY_RUN:
                org_object.save()
