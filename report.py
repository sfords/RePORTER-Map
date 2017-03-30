__author__ = 'sforden'

def getsize(reporter=''):
    import xml.etree.ElementTree as etree
    tree = etree.parse(reporter)
    root = tree.getroot()

    i = 0
    n = 0
    list = []

    while i < len(root):
        for ORG_DUNS in root[i].iter('ORG_DUNS'):
            if ORG_DUNS.text in list:
                n += 0
            elif ORG_DUNS.text == None:
                n += 1
            else:
                list.append(ORG_DUNS.text)
                n += 1
        i += 1

    with open('api_calls.txt', 'a', encoding='utf-8') as api_calls:
        print(reporter, file=api_calls)
        print('projects:', len(root), file=api_calls)
        print('google api calls:', n, '\n', file=api_calls)

def getjson(reporter='D:\PycharmProjects\Re_Map\RePORTER_PRJ_X_FY2014_149.xml'):
    import xml.etree.ElementTree as etree
    import json
    from geocode import getgeo

    tree = etree.parse(reporter)
    root = tree.getroot()

    duns_geo = {}  # hash DUNS: coordinate
    projects = []  # array of individual projects

    i = 0
    while i < len(root):  # iterating through each xml child numbered i
        #  structuring object for later conversion to geojson format

        geometry = {'type': 'Point', 'coordinates': []}
        properties = {'DUNS': '', 'org name': '', 'city': '', 'state': '',
                      'country': '', 'IC': '', 'project': '', 'budget': int(), 'PIs': [], 'terms': []}
        project = {'type': 'Feature','geometry': geometry, 'properties': properties}

        #  parse xml child i, assign properties, and format address for geocoding api calls

        for ORG_NAME in root[i].iter('ORG_NAME'):
            orgName = str(ORG_NAME.text).replace(' ', '+').replace(',', '').replace('.', '')\
                .replace("\u0027", '').replace('\u0026', '+').replace('-', '+')
            properties['org name'] = ORG_NAME.text
        for ORG_DUNS in root[i].iter('ORG_DUNS'):
            duns = ORG_DUNS.text
            properties['DUNS'] = duns
        for IC_NAME in root[i].iter('IC_NAME'):
            properties['IC'] = IC_NAME.text
        for PROJECT_TITLE in root[i].iter('PROJECT_TITLE'):
            properties['project'] = PROJECT_TITLE.text
        for TOTAL_COST in root[i].iter('TOTAL_COST'):
            properties['budget'] = TOTAL_COST.text
        for PI_NAME in root[i].iter('PI_NAME'):
            properties['PIs'].append(PI_NAME.text)
        for ORG_CITY in root[i].iter('ORG_CITY'):
            city = str(ORG_CITY.text).replace(' ', '+')
            properties['city'] = ORG_CITY.text
        for ORG_STATE in root[i].iter('ORG_STATE'):
            state = str(ORG_STATE.text).replace(' ', '+')
            properties['state'] = ORG_STATE.text
        for ORG_ZIPCODE in root[i].iter('ORG_ZIPCODE'):
            zipcode = str(ORG_ZIPCODE.text).replace(' ', '+')
        for ORG_COUNTRY in root[i].iter('ORG_COUNTRY'):
            country = str(ORG_COUNTRY.text).replace(' ', '+')
            properties['country'] = ORG_COUNTRY.text

        if duns in duns_geo:
            #if organization already has coordinate assigned, find coordinate in hash and assign to data structure
            geometry['coordinates'] = duns_geo[duns]
            projects.append(project)

        elif duns == None:
            #if project org has no DUNS, format address for api call

            if state != 'None' and zipcode != 'None':
                address = '{0},{1}+{2},{3}'.format(city, state, zipcode, country)
            elif state == 'None' and zipcode == 'None':
                address = '{0},{1}'.format(city, country)
            elif state == 'None':
                address = '{0},{1},{2}'.format(city, zipcode, country)
            elif zipcode == 'None':
                address = '{0},{1},{2}'.format(city, state, country)

            geo = getgeo(address)  # geocode address
            geometry['coordinates'] = geo  # apply coordinates
            projects.append(project)

        else:
            # if project org has DUNS and doesn't have coordinates already assigned
            if state != 'None' and zipcode != 'None':
                address = '{0},{1},{2}+{3},{4}'.format(orgName, city, state, zipcode, country)
            elif state == 'None' and zipcode == 'None':
                address = '{0},{1}'.format(orgName, city, country)
            elif state == 'None':
                address = '{0},{1},{2}'.format(orgName, city, zipcode, country)
            elif zipcode == 'None':
                address = '{0},{1},{2}'.format(orgName, state, country)

            duns_geo[duns] = getgeo(address)  # assign coordinates to DUNS key42
            geometry['coordinates'] = duns_geo[duns]
            projects.append(project)

        i += 1

    geoproj = {'type': 'FeatureCollection', 'projects': projects}  # final object to be converted to json

    with open('Re{0}1.json'.format(reporter[-8:-4]), 'w', encoding='utf-8') as f:
        json.dump(geoproj, f, indent=3)                            # convert to json in new file
