from math import radians, atan2, atan, cos, sin, asin, sqrt, degrees


# calculate distance betwen two points
# R = 6371 is the radius of earth in kilometers. Use 3956 for miles

def haversine(lat1, lon1, lat2, lon2):

    R = 3959.87433 # this is in miles.  For Earth radius in kilometers use 6372.8 km

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))

    return R * c

def get_bearing(lat1, lon1, lat2, lon2):
    bearing = atan2(sin(lon2-lon1)*cos(lat2), cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(lon2-lon1))
    bearing = degrees(bearing)
    #bearing = (bearing + 360) % 360
    bearing = (bearing + 90) % 360

    return bearing

