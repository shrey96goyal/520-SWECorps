from geopy.geocoders import Nominatim

def convertLocToStr(location):
    locationArray = []
    if location['city'] != '':
        locationArray.append(location['city'])

    if location['state'] != '':
        locationArray.append(location['state'])

    if location['country'] != '':
        locationArray.append(location['country'])

    return ', '.join(locationArray)

# Latitude, Longitude
def getCommonLocation(src_point, dest_point):
    geolocator = Nominatim(user_agent="basicApp3")
    location_src = geolocator.reverse(str(src_point[0]) + ", " + str(src_point[1]))
    location_dest = geolocator.reverse(str(dest_point[0]) + ", " + str(dest_point[1]))
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