# Reads organizations.json and downloads
# detailed organization data from U of I connections.


from urllib import request
import json
import pprint
from app.models import Organization
import html2text


DRY_RUN = False  # dry runs print would-be changes without saving them
DOWNLOAD_ALL = False  # true for production, false for testing when you don't want to download everything
NUM_ORGS = 50  # if DOWNLOAD_ALL is false, only pull this many orgs

pp = pprint.PrettyPrinter()
URL_BASE = 'https://illinois.campuslabs.com/engage/api/discovery/organization/bykey/'

with open('app/scripts/organizations.json') as file:
    organizations = json.load(file)
    for i in range(len(organizations) if DOWNLOAD_ALL else NUM_ORGS):
        org_brief_data = organizations['value'][i]
        response = request.urlopen(URL_BASE + org_brief_data['WebsiteKey'])
        org_data = json.loads(response.read().decode())
        pp.pprint(org_data)

        org_object = Organization(name=org_data['name'],
                                  abbr=(org_data['shortName'] if org_data['shortName'] else None),
                                  found_date=org_data['startDate'],
                                  summary=org_data['summary'],
                                  description=html2text.html2text(org_data['description']) if org_data['description'] else org_data['summary'],
                                  is_public=True,
                                  email=org_data['email'],
                                  last_modified=org_data['modifiedOn'],
                                  is_deleted=org_data['deleted']
                                  )
        if not DRY_RUN:
            org_object.save()
