from geopy.geocoders import Nominatim

'''
    Converts location object to string.
    location - Dictionary with city, state and country as keys
    Returns string in format city, state, country
'''
def convertLocToStr(location):
    print('Converting location object to string')
    locationArray = []
    if location['city'] != '':
        locationArray.append(location['city'])

    if location['state'] != '':
        locationArray.append(location['state'])

    if location['country'] != '':
        locationArray.append(location['country'])

    return ', '.join(locationArray)

'''
    Computes common city, state, country for given points
    srcPoint - [latitude, longitude] of latitude
    destPoint - [latitude, longitude] of longitude
'''
def getCommonLocation(srcPoint, destPoint):
    geolocator = Nominatim(user_agent="basicApp3")
    location_src = geolocator.reverse(str(srcPoint[0]) + ", " + str(srcPoint[1]))
    location_dest = geolocator.reverse(str(destPoint[0]) + ", " + str(destPoint[1]))
    print("Fetched locations!")
    source = location_src.raw['address']
    dest = location_dest.raw['address']
    print("Source Address : {} \nDestination Address : {}".format(source, dest))

    srcCountry = source.get('country','')
    srcState = source.get('state', '')
    srcCity = source.get('city', '')
    if srcCity == '':
        srcCity = source.get('town', '')

    destCountry = dest.get('country', '')
    destState = dest.get('state', '')
    destCity = dest.get('city', '')
    if destCity == '':
        destCity = dest.get('town', '')

    commonLocation = {'country':'', 'state':'', 'city':''}

    print('Checking if country, state and city are same')
    if srcCountry != destCountry:
        return commonLocation
    commonLocation['country'] = srcCountry

    if srcState != destState:
        return commonLocation
    commonLocation['state'] = srcState

    if srcCity != destCity:
        return commonLocation
    commonLocation['city'] = srcCity

    return commonLocation