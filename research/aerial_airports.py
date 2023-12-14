"""
Downloads images of all airports from the Google Static Maps API 
"""

import requests
from parsing_latlong import parsing_latlong

GOOGLEMAPS_API_KEY = "AIzaSyAlvKiF5d2XPTwT1PKpNHd2RUdNXLZxwuI" #API Key here

# -------- Image Setup --------
zoom = "15"
size = "2048x2048"
scale = "2"
format = "png32"
maptype = "satellite"
# ------------------------------

# -------- File Strings --------
airport_data = "../data/GlobalAirportDatabase.txt"
store_folder = "C:/Users/delan/Desktop/APAQ/data/airport_images/"
# ------------------------------

latlong_df = parsing_latlong(airport_data) # get the airport dataframe

latlong_df['combined'] = latlong_df[['lat_dec','long_dec']].apply(lambda row: ','.join(row.values.astype(str)), axis=1) # combine lat and long into one string

# create latlong url
latlong_df['url'] = latlong_df['combined'].apply(lambda x: "https://maps.googleapis.com/maps/api/staticmap?center=" + str(x) + "&zoom=" + zoom + "&size=" + size + "&scale=" + scale + "&format=" + format + "&maptype=" + maptype + "&key=" + GOOGLEMAPS_API_KEY)

# create string for filename 
latlong_df['storage_name'] = latlong_df['airport'].apply(lambda x: store_folder + x + ".png")


# requests implementation
def retreive_images(row) -> None:
    """
    Implements the retrieval of images from given URL to given folder  
    """
    picture_request = requests.get(row['url'])
    if picture_request.status_code == 200:
        with open(row['storage_name'], 'wb') as f:
            f.write(picture_request.content)

# apply requests through dataframe of airports 
latlong_df.apply(lambda row: retreive_images(row),axis =1)


"""
#urllib.request Implemenation: 
import urllib.request
latlong_df.apply(lambda row: urllib.request.urlretrieve(row['url'], row['storage_name']),axis =1)
"""
