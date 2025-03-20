import csv
import os

def add_registration(timestamp: str, name: str, erp: str, year: str, branch: str, phone: int, email: str):
    
    # Check for presence of csv (manual_registration.csv) (should be event name specific) and its structure otherwise trigger code to create one

    if not os.path.exists(r'data\\manual_registration.csv'):        
        data = [
            ['Timestamp', 'Name', 'ERP ID', 'Year', 'Branch', 'Phone Number', 'Email ID'],
        ]

        with open(r'data\\manual_registration.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)

    with open(r'data\\manual_registration.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([[timestamp, name, erp, year, branch, phone, email]])

def add_entry(timestamp: str, erp: str):

    # Check for presence of csv (entries.csv) (should be event name specific) and its structure otherwise trigger code to create one
    
    if not os.path.exists(r'data\\entries.csv'):
        data = [
            ['Timestamp', 'ERP ID'],
        ]

        with open(r'entries.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
    
    with open(r'data\\entries.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([[timestamp, erp]])
    # Any returns?

def load_csv(file_name: str):
    
    # Need to add checks for file existence and related stuff, might need to fix function return type if necessary (also need to see if it's a good practice to have funtions that return varying data types given the situation)
    
    if not os.path.exists(r'data\\{}.csv'.format(file_name)):
        return -1

    with open(r"data\\{}.csv".format(file_name), mode ='r') as file:
        csvFile = csv.reader(file)
        data = list() # Need to see if all entries can be extracted using a single command
        for entry in csvFile:
            data.append(entry[1:])
        del data[0] # Need to see if 0th entry (header row) can be excluded during data entry
    return data
