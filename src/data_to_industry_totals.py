import pandas as pd
import sys
import os


# READ: This program accrues data from the csv's in ~/data/{industry}/{year} and saves the totals of how much each recipient received from
# this industry to a .csv file in ~/data-totals/accumulated-totals/{year}/{industry}-totals.csv as well as
# ~/data-totals/annual-totals/{year}/{industry}-totals.csv.
# The annual-totals file indicates that all of the totals stored in the contained years represent only the totals for that year.
# The accumulated-totals file indicates that all of the totals stored in the contained years represent all of the totals up until that year.


# Given a csv file path, adds its info to the given sector dataframe (oil, hydro, etc.).
def add_csv_info_to_df(csv_file, sector_df) :
    data = pd.read_csv(csv_file)
    for i, j in data.iterrows() :
        if (j.at['Type'] == 'Cand') :
            # print(str(j.at['Recipient']))
            recipient = j.at['Recipient']

            # print(('From Organization' in j) or ('From PACs' in j))
            if ('From PACs' in j) :
                money_entry = j.at['From PACs']
            elif ('From Organization' in j) :
                money_entry = j.at['From Organization']
            else :
                print("A CSV is missing required information.")
                break
            view = j.at['View']
            chamber = j.at['Chamber']
            money_received = int((money_entry.replace('$','')).replace(',',''))
            if (money_received > 0) :
                if (recipient in sector_df.index) :
                    sector_df.loc[recipient] = [int(sector_df.loc[recipient, 'Total']) + money_received, view, chamber]
                    # sector_dict[recipient] = sector_dict[recipient] + money_received
                else :
                    sector_df.loc[recipient] = [money_received, view, chamber]


# The industries we wish to collect data on.
industry_list = ['coal', 'hydro', 'nuclear', 'oil', 'solar', 'wind']


current_directory = os.getcwd()
current_directory = current_directory.replace('\\', '/')


# Goes through .csv files (stored in /data/) with info from OpenSecrets to get annual totals.
for industry in industry_list :
    # industry_dictionary = {}

    # Stores accumulated up until each cycle.
    # industry_df = pd.DataFrame(columns = ['Recipient', 'Total', 'Party', 'Chamber']).set_index('Recipient')
    # industry_dictionary = {}
    # Loops through each year in the industry file and each csv in the year file and collects totals for each recipient.
    # Only loops through cycles from 2010-2020.
    for i in range (10, 21, 2) :
        industry_df = pd.DataFrame(columns = ['Recipient', 'Total', 'Party', 'Chamber']).set_index('Recipient')
        target_directory = current_directory + "/data/" + industry + "/20" + str(i)  
        directory = os.fsencode(target_directory)
        # Code from stackoverflow helped with looping through files in a directory.
        # Link: https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".csv") :
                path_to_file = os.path.join(os.fsdecode(directory), filename)
                add_csv_info_to_df(path_to_file, industry_df)
                continue
            else:
                continue

        # Saves this info to a .csv file in ~/data-totals/annual-totals/{year}/{industry}-totals.csv
        output_string = industry + "-totals"

        path_to_save_to = current_directory + "/data-totals/annual-totals/20" + str(i) + "/" + output_string + ".csv"
        # print(str(industry_dictionary))
        industry_df.to_csv(path_to_save_to)
        print("\n" + industry + " totals saved to " + path_to_save_to + "\n")

# Goes through industry files to get accumulated totals.
for industry in industry_list :
    # industry_dictionary = {}

    # Stores accumulated up until each cycle.
    for cap in range(10, 21, 2) :
        industry_df = pd.DataFrame(columns = ['Recipient', 'Total', 'Party', 'Chamber']).set_index('Recipient')
        # industry_dictionary = {}
        # Loops through each year in the industry file and each csv in the year file and collects totals for each recipient.
        # Only loops through cycles from 2010-2020.
        for i in range (10, cap + 1, 2) :
            target_directory = current_directory + "/data/" + industry + "/20" + str(i)  
            directory = os.fsencode(target_directory)
            # Code from stackoverflow helped with looping through files in a directory.
            # Link: https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                if filename.endswith(".csv") :
                    path_to_file = os.path.join(os.fsdecode(directory), filename)
                    add_csv_info_to_df(path_to_file, industry_df)
                    continue
                else:
                    continue
            

        # Saves this info to a .csv file in ~/data-totals/accumulated-totals/{year}/{industry}-totals.csv
        output_string = industry + "-totals"

        path_to_save_to = current_directory + "/data-totals/accumulated-totals/20" + str(cap) + "/" + output_string + ".csv"
        # print(str(industry_dictionary))
        industry_df.to_csv(path_to_save_to)
        print("\n" + industry + " totals saved to " + path_to_save_to + "\n")
