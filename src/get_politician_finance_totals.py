import sys
import os
import pandas as pd


# READ: This file goes through each industry file located in /data-totals/{accumulated-totals/annual-totals}/{year}/
# and accumulates the information from these 6 files into one totals file stored in
# /data-totals/{accumulated-totals/annual-totals}/year/final-totals/totals.csv
# Also stores a ratios.csv file, but this ended up not being used.

# Adds recipients from the csv file to the given list.
def add_recipients(csv_file, recipient_list) :
    data = (pd.read_csv(csv_file)).set_index('Recipient')
    for i, j in data.iterrows() :
        # CHECK HERE FOR ERROR
        # print(i)
        recipient = str(i)
        if (recipient not in recipient_list) :
            recipient_list.append(recipient)

# Gets the total amount recieved by the recipient from the given file. 
def get_total_for_recipient(recipient, file_path) :
    data = pd.read_csv(file_path).set_index('Recipient')

    #print(data.columns.values.tolist())
    amount = 0
    if recipient in data.index :
        #print(str(data.loc[recipient, '0']))
        amount = int(data.loc[recipient, 'Total'])
        party = str(data.loc[recipient, 'Party'])
        chamber = str(data.loc[recipient, 'Chamber'])
    #for i, j in data.iterrows() :
    #    rec = str(j[0])
    #    if (recipient == rec) :
    #        amount = int(j[1])
    #    print("HERE", amount, party, chamber)
        return [amount, party, chamber]

current_directory = os.getcwd()
current_directory = current_directory.replace('\\', '/')
target_directory = current_directory + "/data-totals"

# Goes through to calculate final-totals for annual-totals.
for year in range(10, 21, 2) :
    directory = os.fsencode(target_directory + "/annual-totals/20" + str(year))


    all_recipients = []

    # Code from stackoverflow helped to loop through files in a directory.
    # Link: https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
    for file in os.listdir(directory) :
        filename = os.fsdecode(file)
        if (filename.endswith(".csv")) :
            path_to_file = os.path.join(os.fsdecode(directory), filename)
            add_recipients(path_to_file, all_recipients)

    zero_list = []
    for r in all_recipients :
        zero_list.append(0)

    df = pd.DataFrame({'Recipient' : all_recipients, 'Party' : list(zero_list), 'Chamber' : list(zero_list), 'Coal Total' : list(zero_list),
        'Hydro Total' : list(zero_list), 'Nuclear Total' : list(zero_list), 'Oil Total' : list(zero_list),
        'Solar Total' : list(zero_list), 'Wind Total' : list(zero_list)}).set_index('Recipient')
    df_ratio = pd.DataFrame({'Recipient' : all_recipients, 'Party' : list(zero_list), 'Chamber' : list(zero_list), 'Coal Ratio' : list(zero_list),
        'Hydro Ratio' : list(zero_list), 'Nuclear Ratio' : list(zero_list), 'Oil Ratio' : list(zero_list), 
        'Solar Ratio' : list(zero_list), 'Wind Ratio' : list(zero_list)}).set_index('Recipient')         


    for recipient in all_recipients :
        for file in os.listdir(directory) :
            filename = os.fsdecode(file)
            if (filename.endswith(".csv")) :
                path_to_file = os.path.join(os.fsdecode(directory), filename)
                if 'coal' in filename :
                    info_list = get_total_for_recipient(recipient, path_to_file)
                    if (info_list) :
                        df.loc[[recipient], ['Coal Total']] = info_list[0]
                        df.loc[[recipient], ['Party']] = info_list[1]
                        df.loc[[recipient], ['Chamber']] = info_list[2]
                elif 'hydro' in filename :
                    info_list = get_total_for_recipient(recipient, path_to_file)
                    if (info_list) :
                        df.loc[[recipient], ['Hydro Total']] = info_list[0]
                        df.loc[[recipient], ['Party']] = info_list[1]
                        df.loc[[recipient], ['Chamber']] = info_list[2]
                elif 'nuclear' in filename :
                    info_list = get_total_for_recipient(recipient, path_to_file)
                    if (info_list) :    
                        df.loc[[recipient], ['Nuclear Total']] = info_list[0]
                        df.loc[[recipient], ['Party']] = info_list[1]
                        df.loc[[recipient], ['Chamber']] = info_list[2]
                elif 'oil' in filename :
                    info_list = get_total_for_recipient(recipient, path_to_file)
                    if (info_list) :    
                        df.loc[[recipient], ['Oil Total']] = info_list[0]
                        df.loc[[recipient], ['Party']] = info_list[1]
                        df.loc[[recipient], ['Chamber']] = info_list[2]
                elif 'solar' in filename :
                    info_list = get_total_for_recipient(recipient, path_to_file)
                    if (info_list) :
                        df.loc[[recipient], ['Solar Total']] = info_list[0]
                        df.loc[[recipient], ['Party']] = info_list[1]
                        df.loc[[recipient], ['Chamber']] = info_list[2]
                elif 'wind' in filename :
                    info_list = get_total_for_recipient(recipient, path_to_file)
                    if (info_list) :    
                        df.loc[[recipient], ['Wind Total']] = info_list[0]
                        df.loc[[recipient], ['Party']] = info_list[1]
                        df.loc[[recipient], ['Chamber']] = info_list[2]


    df["Total"] = (df.drop(columns = ['Party', 'Chamber'])).sum(axis=1)

    for i, j in df.iterrows() :
        # print(str(i), str(j))
        coal_amount = float(j['Coal Total'])
        hydro_amount = float(j['Hydro Total'])
        nuclear_amount = float(j['Nuclear Total'])
        oil_amount = float(j['Oil Total'])
        solar_amount = float(j['Solar Total'])
        wind_amount = float(j['Wind Total'])
        total_amount = float(j['Total'])
        if (total_amount > 0) :
            df_ratio.loc[[i], ['Coal Ratio']] = float(coal_amount / total_amount)
            df_ratio.loc[[i], ['Hydro Ratio']] = float(hydro_amount / total_amount) 
            df_ratio.loc[[i], ['Nuclear Ratio']] = float(nuclear_amount / total_amount) 
            df_ratio.loc[[i], ['Oil Ratio']] = float(oil_amount / total_amount) 
            df_ratio.loc[[i], ['Solar Ratio']] = float(solar_amount / total_amount) 
            df_ratio.loc[[i], ['Wind Ratio']] = float(wind_amount / total_amount) 


    path_to_save_df_to = current_directory + "/data-totals/annual-totals/20" + str(year) + "/final-totals/totals.csv"

    df.to_csv(path_to_save_df_to)

    print("\n" + "Totals saved to " + path_to_save_df_to + "\n")

    path_to_save_ratios_to = current_directory + "/data-totals/annual-totals/20" + str(year) + "/final-totals/ratios.csv"

    df_ratio.to_csv(path_to_save_ratios_to)

    print("\n" + "Ratios saved to " + path_to_save_ratios_to + "\n")

# Goes through to calculate final-totals for accumulated-totals.
for year in range(10, 21, 2) :
    directory = os.fsencode(target_directory + "/accumulated-totals/20" + str(year))


    all_recipients = []

    # Code from stackoverflow helped to loop through files in a directory.
    # Link: https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
    for file in os.listdir(directory) :
        filename = os.fsdecode(file)
        if (filename.endswith(".csv")) :
            path_to_file = os.path.join(os.fsdecode(directory), filename)
            add_recipients(path_to_file, all_recipients)

    zero_list = []
    for r in all_recipients :
        zero_list.append(0)

    df = pd.DataFrame({'Recipient' : all_recipients, 'Party' : list(zero_list), 'Chamber' : list(zero_list), 'Coal Total' : list(zero_list),
        'Hydro Total' : list(zero_list), 'Nuclear Total' : list(zero_list), 'Oil Total' : list(zero_list),
        'Solar Total' : list(zero_list), 'Wind Total' : list(zero_list)}).set_index('Recipient')
    df_ratio = pd.DataFrame({'Recipient' : all_recipients, 'Party' : list(zero_list), 'Chamber' : list(zero_list), 'Coal Ratio' : list(zero_list),
        'Hydro Ratio' : list(zero_list), 'Nuclear Ratio' : list(zero_list), 'Oil Ratio' : list(zero_list), 
        'Solar Ratio' : list(zero_list), 'Wind Ratio' : list(zero_list)}).set_index('Recipient')         


    for recipient in all_recipients :
        for file in os.listdir(directory) :
            filename = os.fsdecode(file)
            if (filename.endswith(".csv")) :
                path_to_file = os.path.join(os.fsdecode(directory), filename)
                if 'coal' in filename :
                    info_list = get_total_for_recipient(recipient, path_to_file)
                    if (info_list) :
                        df.loc[[recipient], ['Coal Total']] = info_list[0]
                        df.loc[[recipient], ['Party']] = info_list[1]
                        df.loc[[recipient], ['Chamber']] = info_list[2]
                elif 'hydro' in filename :
                    info_list = get_total_for_recipient(recipient, path_to_file)
                    if (info_list) :
                        df.loc[[recipient], ['Hydro Total']] = info_list[0]
                        df.loc[[recipient], ['Party']] = info_list[1]
                        df.loc[[recipient], ['Chamber']] = info_list[2]
                elif 'nuclear' in filename :
                    info_list = get_total_for_recipient(recipient, path_to_file)
                    if (info_list) :    
                        df.loc[[recipient], ['Nuclear Total']] = info_list[0]
                        df.loc[[recipient], ['Party']] = info_list[1]
                        df.loc[[recipient], ['Chamber']] = info_list[2]
                elif 'oil' in filename :
                    info_list = get_total_for_recipient(recipient, path_to_file)
                    if (info_list) :    
                        df.loc[[recipient], ['Oil Total']] = info_list[0]
                        df.loc[[recipient], ['Party']] = info_list[1]
                        df.loc[[recipient], ['Chamber']] = info_list[2]
                elif 'solar' in filename :
                    info_list = get_total_for_recipient(recipient, path_to_file)
                    if (info_list) :
                        df.loc[[recipient], ['Solar Total']] = info_list[0]
                        df.loc[[recipient], ['Party']] = info_list[1]
                        df.loc[[recipient], ['Chamber']] = info_list[2]
                elif 'wind' in filename :
                    info_list = get_total_for_recipient(recipient, path_to_file)
                    if (info_list) :    
                        df.loc[[recipient], ['Wind Total']] = info_list[0]
                        df.loc[[recipient], ['Party']] = info_list[1]
                        df.loc[[recipient], ['Chamber']] = info_list[2]


    df["Total"] = (df.drop(columns = ['Party', 'Chamber'])).sum(axis=1)

    for i, j in df.iterrows() :
        # print(str(i), str(j))
        coal_amount = float(j['Coal Total'])
        hydro_amount = float(j['Hydro Total'])
        nuclear_amount = float(j['Nuclear Total'])
        oil_amount = float(j['Oil Total'])
        solar_amount = float(j['Solar Total'])
        wind_amount = float(j['Wind Total'])
        total_amount = float(j['Total'])
        if (total_amount > 0) :
            df_ratio.loc[[i], ['Coal Ratio']] = float(coal_amount / total_amount)
            df_ratio.loc[[i], ['Hydro Ratio']] = float(hydro_amount / total_amount) 
            df_ratio.loc[[i], ['Nuclear Ratio']] = float(nuclear_amount / total_amount) 
            df_ratio.loc[[i], ['Oil Ratio']] = float(oil_amount / total_amount) 
            df_ratio.loc[[i], ['Solar Ratio']] = float(solar_amount / total_amount) 
            df_ratio.loc[[i], ['Wind Ratio']] = float(wind_amount / total_amount) 


    path_to_save_df_to = current_directory + "/data-totals/accumulated-totals/20" + str(year) + "/final-totals/totals.csv"

    df.to_csv(path_to_save_df_to)

    print("\n" + "Totals saved to " + path_to_save_df_to + "\n")

    path_to_save_ratios_to = current_directory + "/data-totals/accumulated-totals/20" + str(year) + "/final-totals/ratios.csv"

    df_ratio.to_csv(path_to_save_ratios_to)

    print("\n" + "Ratios saved to " + path_to_save_ratios_to + "\n")

