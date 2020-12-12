import json
import requests
import pandas as pd
from pandas.io.json import json_normalize


# Note this is specific to the congress api
congress_api = "https://api.propublica.org/congress/v1/bills/subjects/energy.json"

congress_api_key = "YOUR API KEY HERE"
congress_headers = {
    # 'Content-Type': 'application/json',
    'X-API-Key': congress_api_key}

# TODO: Are there any other synonyms that people want?
sectors = ["oil", "petroleum", "natural gas", "gas", "solar", "wind", "hydro", "hydroelectric", "nuclear", "coal"]

def get_next_page(offset):
    print("Getting page with offset:", offset)
    response = requests.get(congress_api + "?offset=" + str(offset), headers=congress_headers)
    print(response)
    return response.json()


def get_all_bills(min_date):
    irrelevant_count = 0
    all_bills = []
    i = 0
    while True:
        curr_page = get_next_page(i)
        results = curr_page["results"]

        print(len(results))
        for bill in results:
            date = bill["introduced_date"]
            date_int = int(date[0:4])
            if date_int < min_date:
                print("Got all the bills we need")
                return all_bills, irrelevant_count
            else:
                summary = bill["summary"]
                # Note: Currently adding empty summaries because I think we should investigate
                if summary == None or contains_sector(summary, sectors):
                    all_bills.append(bill)
                else:
                    irrelevant_count += 1
                    print("Bill did not contain relevant sectors")
        i += 20 # Page size is 20
    return all_bills, irrelevant_count

# Does the string (assumed to be a summary) contain at least one of the sectors we are looking for
# sectors is assumed to be a list of strings
def contains_sector(summary, sectors):
    # print("Summary:", summary)
    return any(s in summary for s in sectors)



all_bills, irrelevant_count = get_all_bills(2008)

print("irrelevant_count:", irrelevant_count)

all_df = pd.DataFrame(all_bills)

print(all_df.head())

limited_df = pd.DataFrame()

limited_df['bill_id'] = all_df['bill_id']
limited_df['congressdotgov_url'] = all_df['congressdotgov_url']
limited_df['govtrack_url'] = all_df['govtrack_url']
limited_df['title'] = all_df['title']
limited_df['summary'] = all_df['summary']

### ADDING SECTORS
limited_df['oil'] = 0
limited_df['solar'] = 0
limited_df['wind'] = 0
limited_df['hydro'] = 0
limited_df['nuclear'] = 0
limited_df['coal'] = 0

limited_df.to_csv("bills_limited.csv")
all_df.to_csv("all_bills.csv")




