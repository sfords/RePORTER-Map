__author__ = 'sforden'

def getgeo(address, key=''): #requires google api key
    import urllib.request
    import urllib.parse
    import xml.etree.ElementTree as etree
    import time

    url = 'https://maps.googleapis.com/maps/api/geocode/xml?address={0}&key={1}'.format(address, key)
    print(url)
    u = urllib.request.urlopen(url, data=None)

    tree = etree.parse(u)
    root = tree.getroot()

    for status in root:
        if status.text == 'ZERO_RESULTS':  # coordinates could not be found
            return None

        elif status.text == 'OK':
            for location in root.iter('location'):
                for lat in location.findall('lat'):
                    latt = float(lat.text)
            for location in root.iter('location'):
                for lng in location.findall('lng'):
                    long = float(lng.text)
            geo = [long, latt]
            return geo

    time.sleep(0.11)