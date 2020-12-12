import json
import requests
import pandas as pd
from pandas.io.json import json_normalize

chambers = {"house", "senate"}
starting_session = 110
ending_session = 116
all_members = []

congress_api_key = "## INSERT YOUR API KEY HERE"
congress_headers = {
    'X-API-Key': congress_api_key}

desired_information = ["name", "session", "chamber", "party", "fec_candidate_id", "id", "crp_id"]


def get_response(chamber, session):
    """
        Get the next page of the api.
    """
    congress_api = f"https://api.propublica.org/congress/v1/{session}/{chamber}/members.json"
    response = requests.get(congress_api, headers=congress_headers)
    return response.json()


def get_congress_members(chamber, session):
    response = get_response(chamber, session)
    results = response["results"]
    session_members = []
    for result in results:
        members = result["members"]
    
        for member in members:
            first_name = member["first_name"]
            last_name = member["last_name"]
            chamber = member["short_title"]
            party = member["party"]
            fec_candidate_id = member["fec_candidate_id"]
            idnum = member["id"]
            crpid = member["crp_id"]
            result = {"name": f"{first_name} {last_name}", "session": f"{session}", "chamber": f"{chamber}", "party": f"{party}", "fec_candidate_id": f"{fec_candidate_id}", "id": f"{idnum}", "crp_id": f"{crpid}"}
            session_members.append(result)
            print(result)
    return session_members

def get_all_congress_members():
    all_members = []
    for cur_chamber in chambers:
        for session in range(starting_session, ending_session + 1):
            current_members = get_congress_members(cur_chamber, session)
            for member in current_members:
                all_members.append(member)
    return all_members

all_members = get_all_congress_members()
all_member_df = pd.DataFrame(all_members)
all_member_df.to_csv("members.csv")
print("finished: ", len(all_members))

