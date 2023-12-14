import pandas as pd

def parsing_latlong(filename) -> pd.DataFrame:

    with open(filename, newline="") as f:
        data = pd.read_csv(f,sep = ":",header = None)

    lat_degrees = data[5].astype(float)
    lat_minutes = data[6].astype(float)
    lat_seconds = data[7].astype(float)
    data["direction_lat"] = data[8]

    long_degrees = data[9].astype(float)
    long_minutes = data[10].astype(float)
    long_seconds = data[11].astype(float)
    data["direction_long"] = data[12]

    # calculate latitute and longitude, save airport name
    data["lat_dec"] = lat_degrees + lat_minutes/60 + lat_seconds/(60*60)
    data["long_dec"]  = long_degrees + long_minutes/60 + long_seconds/(60*60)
    data["airport"] = data[2]

    #drop null values 
    longlat_data = data[['airport','lat_dec','long_dec','direction_lat','direction_long']].dropna()

    #drop null directions
    longlat_data = longlat_data[longlat_data.direction_lat != "U"]
    longlat_data = longlat_data[longlat_data.direction_long != "U"]

    #add negatives and positives to longitude data based on direction
    longlat_data.loc[longlat_data['direction_lat'] == "S", 'lat_dec'] = -1*longlat_data["lat_dec"] 
    longlat_data.loc[longlat_data['direction_long'] == "W", 'long_dec'] = -1*longlat_data["long_dec"] 
    longlat_data = longlat_data.drop(["direction_lat","direction_long"], axis=1).reset_index(drop=True)
    
    longlat_data = longlat_data.replace(" ", "_", regex=True)

    return longlat_data
