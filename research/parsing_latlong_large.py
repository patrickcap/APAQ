import pandas as pd

def parsing_latlong(filename) -> pd.DataFrame:

    with open(filename, newline="",encoding="utf-8") as f:
        data = pd.read_csv(f,sep = ",")


    # calculate latitute and longitude, save airport name
    data["lat_dec"] = data.iloc[:, 5]#.astype(float) 
    data["long_dec"]  = data.iloc[:, 6]#.astype(float)
    data["airport"] = data.iloc[:, 2]

    #drop null values 
    longlat_data = data[["airport","lat_dec","long_dec"]].dropna()

    return longlat_data
