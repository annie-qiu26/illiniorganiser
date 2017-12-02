from urllib import request
import json
import pprint
from app.models import Organization, OrganizationPosition
from django.contrib.auth.models import User


DRY_RUN = True  # dry runs print would-be changes without saving them
DOWNLOAD_ALL = False  # true for production, false for testing when you don't want to download everything
NUM_ORGS = 50  # if DOWNLOAD_ALL is false, only pull this many orgs

pp = pprint.PrettyPrinter()
URL_BASE = 'https://illinois.campuslabs.com/engage/api/discovery/organization/'
URL_END = '/position?take=100'

with open('app/scripts/organizations.json') as file:
    organizations = json.load(file)
    for i in range(len(organizations) if DOWNLOAD_ALL else NUM_ORGS):
        organization_data = organizations['value'][i]
        url = URL_BASE + str(organization_data['Id']) + URL_END
        response = request.urlopen(url)

        print()
        print(url)

        positions = json.loads(response.read().decode())['items']
        # pp.pprint(positions)

        organization = Organization.objects.get(name=organization_data['Name'])
        print(organization)
        print('=' * len(str(organization)))

        for position_data in positions:
            position_type = 'M'
            type_name = position_data['typeName']
            if type_name == 'Student Organization Advisor':
                position_type = 'F'
            elif type_name == 'Student Organization Officer' or type_name == 'Primary Contact':
                position_type = 'A'
            elif type_name == 'Member / Participant':
                position_type = 'M'
            else:
                print('Weird position type:')
                print('=====================================')
                pp.pprint(position)
                print('=====================================')
            position = OrganizationPosition(name=position_data['name'].strip(),
                                            type=position_type,
                                            organization=organization
                                            )

            print('Added position:', position, 'of type:', position_type)

            if not DRY_RUN:
                position.save()

            for holder in position_data['holders']:
                user = User(username=holder['primaryEmailAddress'].lower(),
                            first_name=holder['firstName'],
                            last_name=holder['lastName']
                            )
                print('  Added user:', user)

                if not DRY_RUN:
                    user.save()