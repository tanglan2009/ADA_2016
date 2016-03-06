# Question 3:
# In which year (1957 or 2007) did storms have a higher monetary impact
# within the boundaries of the Louisiana Purchase territory?

## result
##  monetary impact in 2007 1465466 K
##  monetary impact in 1957 111794 K
## In 2007,storms had a higher monetary impact within the boundaries of the Louisiana Purchase territory.

# Strategy: 1) find the geometry kml data (Louisiana Purchase 1803.kml) for Louisiana Purchase Territory boundary
# 2) download the data and convert to geojson data (Louisiana.json)
#           3) Load Louisiana.json in Shapely, and create a shape object for Louisiana_Purchase_Territory
#           4) create point objects: Point(longitude, latitude), check whether point in shape with the built-in function.

import json
from shapely.geometry import Point, shape
import csv

data = json.loads(open("Louisiana.json").read())
Louisiana_Purchase_Territory = data['geometry']

# check point in the geometry shape
# point = Point(-109.18, 41.58)
# print shape(Louisiana_Purchase_Territory_shape ).contains(point)

def string_start_with_vowels(string):
    vowels = 'AEIOUaeiou'
    for char in vowels:
        if string.startswith(char):
            return True
    return False


#
file1957 = "StormEvents_details-ftp_v1.0_d1957_c20160223.csv"
file2007 = "StormEvents_details-ftp_v1.0_d2007_c20160223.csv"

# convert money with unit 'M' to 'K', if empty or non-number return 0
def convert_money(amount_of_money):
    try:
        if "M" in amount_of_money:
            amount_of_money = float(amount_of_money.strip().replace("M", "")) * 1000
        elif "K" in amount_of_money:
            amount_of_money = float(amount_of_money.strip().replace("K", ""))
        else:
            amount_of_money = float(amount_of_money)
    # filter out rows with non-number or empty string
    except:
        return 0
    return amount_of_money


# get the total monetary impact from file
def total_monetary_impact_per_year(file):
    with open(file) as f:
        reader = csv.DictReader(f)
        total_damage_property = 0
        total_damage_crops = 0

        for row in reader:
            try:
                lat = float(row['BEGIN_LAT'])
                lon = float(row['BEGIN_LON'])
                point = Point(lon, lat)
                if not (string_start_with_vowels(row["CZ_NAME"])) and \
                        shape(Louisiana_Purchase_Territory).contains(point):
                    total_damage_property += convert_money(row["DAMAGE_PROPERTY"])
                    total_damage_crops += convert_money(row["DAMAGE_CROPS"])



            # filter out rows with empty string(none value) for "BEGIN_LON" or "BEGIN_LAT"
            except ValueError:
                continue
    return total_damage_property + total_damage_crops


print"monetary impact in 2007 %d K" % (total_monetary_impact_per_year(file2007))
print"monetary impact in 1957 %d K" % (total_monetary_impact_per_year(file1957))
#

print"in 2007,storms had a higher monetary impact within the boundaries of the Louisiana Purchase territory."
