"""
Downloads images of all airports from the Google Static Maps API 
"""

import requests
from parsing_latlong_large import parsing_latlong


# -------- Image Setup --------
zoom = "15"
size = "2048x2048"
scale = "2"
format = "png32"
maptype = "satellite"
# ------------------------------

# -------- File Strings --------
airport_data = "../data/iata-icao.csv"
# ------------------------------


GOOGLEMAPS_API_KEY = input("Enter your Google Static Maps API key: ") 
store_folder = input("Enter the directory you want to store the images to: ") #C:/Users/delan/Desktop/APAQ/data/airport_images/

latlong_df = parsing_latlong(airport_data) # get the airport dataframe

latlong_df["combined"] = latlong_df[["lat_dec","long_dec"]].apply(lambda row: ",".join(row.values.astype(str)), axis=1) # combine lat and long into one string

# create latlong url
latlong_df["url"] = latlong_df["combined"].apply(lambda x: "https://maps.googleapis.com/maps/api/staticmap?center=" + str(x) + "&zoom=" + zoom + "&size=" + size + "&scale=" + scale + "&format=" + format + "&maptype=" + maptype + "&key=" + GOOGLEMAPS_API_KEY)

# create string for filename 
latlong_df["storage_name"] = latlong_df["airport"].apply(lambda x: store_folder + x + ".png")

# apply requests through dataframe of airports
def apply_image_request(df, i, j) -> None:
    df_temp = df.iloc[i:j]
    df_temp.apply(lambda row: retrieve_images(row),axis =1)

# requests implementation
def retrieve_images(row) -> None:
    """
    Implements the retrieval of images from given URL to given folder  
    """

    picture_request = requests.get(row["url"])
    if picture_request.status_code == 200:
        with open(row["storage_name"], "wb") as f:
            f.write(picture_request.content)
    else:
         print("Request failed with status code: ", picture_request.status_code)

i = 5649 #0
j = 6000 #1000

#download images in batches 
while (True):
    if j <= 8000:
        print("Batch set: ", i, " to ", j)
        apply_image_request(latlong_df, i, j)
        print("Batch complete")
        i = j
        j = j+1000
    else: #when you reach the end of the dataframe
        i = 8000
        j = 8967
        apply_image_request(latlong_df, i, j)
        break
        






