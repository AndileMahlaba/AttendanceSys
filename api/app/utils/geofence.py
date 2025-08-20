from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on the earth"""
    R = 6371000  # Earth radius in meters
    
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)
    
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    a = sin(dlat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c

def check_geofence(user_lat, user_lon, user_accuracy, venue_lat, venue_lon, venue_radius):
    """Check if user is within venue geofence"""
    if None in (user_lat, user_lon, venue_lat, venue_lon):
        return False, "Missing location data"
    
    distance = haversine_distance(user_lat, user_lon, venue_lat, venue_lon)
    
    # Account for GPS accuracy
    if distance <= (venue_radius + user_accuracy):
        return True, f"Within {int(distance)}m of venue"
    else:
        return False, f"Outside geofence by {int(distance - venue_radius)}m"