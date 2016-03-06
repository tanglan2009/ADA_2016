import csv
file1957 = "StormEvents_details-ftp_v1.0_d1957_c20160223.csv"
file2007 = "StormEvents_details-ftp_v1.0_d2007_c20160223.csv"

# helper function to exclude all rows that have a County/Parish, Zone, or Marine name that begins with a vowel.
def string_start_with_vowels(string):
    vowels = 'AEIOUaeiou'
    for char in vowels:
        if string.startswith(char):
            return True
    return False


# Qestion 1
# 1. How many counties in the state of Washington remained storm free in 2007?
# result
# 17 counties in the state of Washington remained storm free in 2007.
#
# strategy: 1) get a list of counties in washington state
#           2) Read file, check each row, if it satisfies the condition, remove the county name from the list of counties .
#           3) get the length of the counties left (storm-free)


# list of counties in Washington State, obtained from wiki.
countiesList = ["Adams", "Asotin", "Benton", "Chelan", "Clallam", "Clark", "Columbia", "Cowlitz", "Douglas", "Ferry",
                "Franklin", "Garfield", "Grant", "Grays Harbor", "Island", "Jefferson", "King", "Kitsap", "Kittitas",
                "Klickitat", "Lewis", "Lincoln", "Mason", "Okanogan", "Pacific", "Pend Oreille", "Pierce", "San Juan",
                "Skagit", "Skamania", "Snohomish", "Spokane", "Stevens", "Thurston", "Wahkiakum", "Walla Walla",
                "Whatcom", "Whitman", "Yakima"]

# change all counties in uppercase to match the value in 'CZ_NAME" column
countiesList = [county.upper() for county in countiesList]

with open(file2007) as f:
    reader = csv.DictReader(f)  # read rows into a dictionary format

    for row in reader:
        county_name = row["CZ_NAME"].strip().upper()
        state_name = row['STATE'].strip().upper()
        # satisfy Washington state and county_name not start with vowels

        if county_name in countiesList and state_name == 'WASHINGTON' and (not string_start_with_vowels(county_name)):
                countiesList.remove(county_name)



print "%d counties in the state of Washington remained storm free in 2007." % (len( countiesList))



# Question 2
# 2: How many wind based storms happened between 8AM PST and 11AM PST in 1957?
#result
#161 wind based storms happened between 8AM PST and 11AM PST in 1957.


# strategy: 1) get all event types from the file. There are three types of event.
#               skip this step if event types are known
#           2) defined wind based storm types: Tornado and Thunderstorm wind.

# get total event types
event_type = set()
with open(file1957) as f:
    reader = csv.DictReader(f)  # read rows into a dictionary format
    
    for row in reader:
        event_type.add(row['EVENT_TYPE'])
print event_type


def event_type_at_timezone(event_type, begin_time, end_time, data):
    return data['EVENT_TYPE'] in event_type and int(data['BEGIN_TIME']) >= begin_time and int(data['END_TIME']) <= end_time

## time zone in file is CST, so convert 8AM PST and 11AM PST to 1000 CST and 1300 CST respectively.

event_type = ['Tornado', 'Thunderstorm Wind']
with open(file1957) as f:
    reader = csv.DictReader(f)  # read rows into a dictionary format

    # initialize number of wind based storms
    count = 0
    for row in reader:
        if (event_type_at_timezone(event_type, 1000, 1300, row)) and\
                    not(string_start_with_vowels(row["CZ_NAME"])):
            count += 1

print"%d wind based storms happened between 8AM PST and 11AM PST in 1957." % (count)
