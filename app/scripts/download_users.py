# Must be run after download_orgs.py
#
# Reads organizations.json and downloads user data
# from U of I connections. This doesn't include every student
# in the school--only those listed on U of I Connections
# as leaders of RSO's. This script creates associations
# between student leaders and their respective organizations.

from urllib import request
import json
import pprint
from termcolor import cprint
from app.models import Organization, OrganizationPosition, MyUser


DRY_RUN = False  # dry runs print would-be changes without saving them
DOWNLOAD_ALL = False  # true for production, false for testing when you don't want to download everything
ORGS_RANGE = range(0, 100)  # if DOWNLOAD_ALL is false, only pull from this many orgs
RESET = True  # delete all existing regular users (aka not superusers)

pp = pprint.PrettyPrinter()
URL_BASE = 'https://illinois.campuslabs.com/engage/api/discovery/organization/'
URL_END = '/position?take=100'

with open('app/scripts/organizations.json', encoding='utf8') as file:

    if RESET:
        if not DRY_RUN:
            MyUser.objects.filter(is_superuser=False).delete()
        cprint('Deleted all users', 'green')

    organizations = json.load(file)
    organizations_count = 0
    positions_count = 0
    users_count = 0

    for i in (range(len(organizations)) if DOWNLOAD_ALL else ORGS_RANGE):
        organization_data = organizations['value'][i]
        url = URL_BASE + str(organization_data['Id']) + URL_END
        response = request.urlopen(url)

        print()
        print(url)

        positions = json.loads(response.read().decode())['items']
        # pp.pprint(positions)

        organization = Organization.objects.get(name=organization_data['Name'])
        organizations_count += 1

        print(organization)
        print('=' * len(str(organization)))

        for position_data in positions:

            if position_data['holders']:

                type_name = position_data['typeName']
                if type_name == 'Student Organization Advisor':
                    position_type = 'F'
                elif type_name == 'Student Organization Officer' or type_name == 'Primary Contact':
                    position_type = 'A'
                elif type_name == 'Member / Participant':
                    position_type = 'M'
                else:
                    cprint('Weird position type: {}'.format(position_data), 'red')
                    break

                position = OrganizationPosition(name=position_data['name'].strip(),
                                                type=position_type,
                                                organization=organization
                                                )

                positions_count += 1
                print('Added position: {} of type: {}'.format(position, position_type))

                if not DRY_RUN:
                    position.save()

                for holder in position_data['holders']:
                    user, created = MyUser.objects.get_or_create(email=holder['primaryEmailAddress'].lower())
                    if created:
                        user.first_name = holder['firstName']
                        user.last_name = holder['lastName']
                        user.claimed = False
                        users_count += 1
                        print('\t Added user: {}'.format(user))

                        if not DRY_RUN:
                            user.save()
                            position.holders.add(user)
                    else:
                        if not DRY_RUN:
                            position.holders.add(user)


    print()
    cprint('Successfully downloaded {} users in {} positions for {} organizations'.format(users_count,
                                                                                          positions_count,
                                                                                          organizations_count), 'green')
