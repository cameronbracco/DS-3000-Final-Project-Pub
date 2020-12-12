import json
import requests
import pandas as pd
from pandas.io.json import json_normalize


members_df = pd.read_csv("data-totals/member-pac-totals.csv")
members = members_df["id"].to_numpy()
bills_df = pd.read_csv("bills_limited_sectors.csv")
bills_id = set(bills_df["bill_id"].to_numpy())

votes_cast = pd.DataFrame(index=members, columns=bills_id)

congress_api_key = "YOUR API KEY HERE"
congress_headers = {
    'X-API-Key': congress_api_key}

def get_next_page(offset, member_id):
    print("Getting page with offset:", offset)
    congress_api = f"https://api.propublica.org/congress/v1/members/{member_id}/votes.json"
    response = requests.get(congress_api + "?offset=" + str(offset), headers=congress_headers)
    print(response)
    return response.json()


def get_bill_votes(member_id):
    i = 0
    curr_page = get_next_page(i, member_id)
    results = curr_page["results"]
    for result in results:
        votes = result["votes"]
    for vote in votes:
        date = vote["date"]
    year_int = int(date[:4])
    while (year_int >= 2010 and len(votes) > 0):
        curr_page = get_next_page(i, member_id)
        results = curr_page["results"]
        for result in results:
            votes = result["votes"]
    
        for vote in votes:
            bill = vote["bill"]
            date = vote["date"]
            year_int = int(date[:4])
            try:
                bill_id = bill["bill_id"]
            except:
                bill_id = "NOT FOUND"
            position = vote["position"]
            if(bill_id in bills_id):
                print("bill", bill_id, "found for member", member_id)
                votes_cast.at[member_id, bill_id] = position
            else:
                print("not found", bill_id, "for member", member_id)
        i+=20

def get_n_bill_votes(start_index):
    for i in range(start_index, start_index + 5):
        member_id = members[i]
        get_bill_votes(member_id)
    votes_cast.to_csv(f"data-totals/votes/votes-cast-{start_index}.csv")

def get_final_bill_votes(start_index):
    for i in range(start_index, len(members)):
        member_id = members[i]
        get_bill_votes(member_id)
    votes_cast.to_csv(f"data-totals/votes/votes-cast-{start_index}.csv")

def get_all_bill_votes(start, end, increment):
    start_index = start
    for i in range(start_index, end, increment):
        get_n_bill_votes(i)
    #get_final_bill_votes(len(members) - len(members) % 5)


get_all_bill_votes(690, 700, 5)
    

