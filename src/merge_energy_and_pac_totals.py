import os
import sys
import pandas as pd


# Takes a name from the pac data and a name from the totals data and sees if they match.
def name_match(pac_name, totals_name) :
    totals_name = totals_name.strip()
    totals_name_list = totals_name.split(" ")
    updated_totals_name = totals_name_list[0] + " " + totals_name_list[1]
    pac_name = pac_name.strip()
    pac_name_list = pac_name.split(" ")
    updated_pac_name = pac_name_list[1] + ", " + pac_name_list[0]
    # print(":" + updated_pac_name + ": VS :" + updated_totals_name + ":")
    if (updated_pac_name == updated_totals_name) :
        print("Same name")
        return True
    else :
        return False

# Function that goes through either accumulated totals and 
def merge_in_directory(directory_name, pac_df) : 

    pac_data = pd.read_csv(target_directory + "/member-pac-totals.csv").set_index('name')
    for year in range(10, 21, 2) :
        directory = os.fsencode(directory_name + "/20" + str(year) + "/final-totals")
                #+ "/final-totals/totals.csv")
        filename = os.path.join(os.fsdecode(directory), "totals.csv")
        totals_df = pd.read_csv(filename.replace('\\', '/')).set_index('Recipient')
        totals_df["PAC Total"] = ""
        totals_df["FEC Candidate ID"] = ""
        totals_df["ID"] = ""
        for index, row_content in totals_df.iterrows() :
            print ("Searching for " + index)
            for pac_index, pac_content in pac_data.iterrows() :
                if name_match(pac_index, index) :
                    totals_df.loc[[index], ['PAC Total']] = pac_data.loc[pac_index, "20" + str(year)]
                    totals_df.loc[[index], ['FEC Candidate ID']] = pac_data.loc[pac_index, "fec_candidate_id"]
                    totals_df.loc[[index], ['ID']] = pac_data.loc[pac_index, "id"]

        totals_df = totals_df[totals_df['PAC Total'] != ""]

        totals_df["Coal Ratio"] = 0
        totals_df["Hydro Ratio"] = 0
        totals_df["Nuclear Ratio"] = 0
        totals_df["Oil Ratio"] = 0
        totals_df["Solar Ratio"] = 0
        totals_df["Wind Ratio"] = 0
        industries = ["Coal", "Hydro", "Nuclear", "Oil", "Solar", "Wind"]
        for i, j in totals_df.iterrows() :
            if (float(totals_df.loc[i, "PAC Total"]) > 0) :
                print("Greater than zero")
                for industry in industries :
                    totals_df.loc[[i], [industry + " Ratio"]] = float(totals_df.loc[i, industry + " Total"]) / float(totals_df.loc[i, "PAC Total"])
            elif (float(totals_df.loc[i, "PAC Total"]) == 0) :
                totals_df.loc[[i], ["PAC Total"]] = float(totals_df.loc[i, 'Total'])
                for industry in industries :
                    totals_df.loc[[i], [industry + " Ratio"]] = float(totals_df.loc[i, industry + " Total"]) / float(totals_df.loc[i, "PAC Total"])

        totals_df.to_csv(filename)
        print("\n" + "Totals saved to " + filename + "\n")


def merge_in_directory_accumulate(directory_name, pac_df) : 
    pac_data = pd.read_csv(target_directory + "/member-pac-totals.csv").set_index('name')
    for cap in range(10, 21, 2) :
        directory = os.fsencode(directory_name + "/20" + str(cap) + "/final-totals")
                #+ "/final-totals/totals.csv")
        filename = os.path.join(os.fsdecode(directory), "totals.csv")
        totals_df = pd.read_csv(filename.replace('\\', '/')).set_index('Recipient')
        totals_df["PAC Total"] = ""
        totals_df["FEC Candidate ID"] = ""
        totals_df["ID"] = ""
        for year in range(10, cap + 1, 2) :
            for index, row_content in totals_df.iterrows() :
                print ("Searching for " + index)
                for pac_index, pac_content in pac_data.iterrows() :
                    if name_match(pac_index, index) :
                        if (totals_df.loc[index, 'PAC Total'] == "") :
                            totals_df.loc[[index], ['PAC Total']] = pac_data.loc[pac_index, "20" + str(year)]
                        else :
                            totals_df.loc[[index], ['PAC Total']] = float(totals_df.loc[index, 'PAC Total']) + float(pac_data.loc[pac_index, "20" + str(year)])
                        totals_df.loc[[index], ['FEC Candidate ID']] = pac_data.loc[pac_index, "fec_candidate_id"]
                        totals_df.loc[[index], ['ID']] = pac_data.loc[pac_index, "id"]

        totals_df = totals_df[totals_df['PAC Total'] != ""]

        totals_df["Coal Ratio"] = 0
        totals_df["Hydro Ratio"] = 0
        totals_df["Nuclear Ratio"] = 0
        totals_df["Oil Ratio"] = 0
        totals_df["Solar Ratio"] = 0
        totals_df["Wind Ratio"] = 0
        industries = ["Coal", "Hydro", "Nuclear", "Oil", "Solar", "Wind"]
        for i, j in totals_df.iterrows() :
            if (float(totals_df.loc[i, "PAC Total"]) > 0) :
                print("Greater than zero")
                for industry in industries :
                    totals_df.loc[[i], [industry + " Ratio"]] = float(totals_df.loc[i, industry + " Total"]) / float(totals_df.loc[i, "PAC Total"])
            elif (float(totals_df.loc[i, "PAC Total"]) == 0) :
                totals_df.loc[[i], ["PAC Total"]] = float(totals_df.loc[i, 'Total'])
                for industry in industries :
                    totals_df.loc[[i], [industry + " Ratio"]] = float(totals_df.loc[i, industry + " Total"]) / float(totals_df.loc[i, "PAC Total"])

        totals_df.to_csv(filename)
        print("\n" + "Totals saved to " + filename + "\n")


# Get PAC csv.

current_directory = os.getcwd()
current_directory = current_directory.replace('\\', '/')
target_directory = current_directory + "/data-totals"

pac_data = pd.read_csv(target_directory + "/member-pac-totals.csv")

merge_in_directory_accumulate(target_directory + "/accumulated-totals", pac_data)
merge_in_directory(target_directory + "/annual-totals", pac_data)











