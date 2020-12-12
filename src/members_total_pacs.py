## Quick file to use members.csv and get their contribution totals for each cycle
import pandas as pd
import requests

# Ideal output csv
# Name, ProPublic ID?, party, 2010, 2012, 2014, 2016, 2018, 2020 (amount from pacs)

campaign_finance_api_key = "YOUR API KEY HERE"
campaign_finance_headers = {
    'X-API-Key': campaign_finance_api_key
}


def get_candidate(fec_id, cycle):
    """
        TODO: Documentation
    """
    finance_api = f"https://api.propublica.org/campaign-finance/v1/{cycle}/candidates/{fec_id}.json"
    response = requests.get(finance_api, headers=campaign_finance_headers)
    if response.status_code == 200:
        # print(response)
        return response.json()
    else:
        print("Bad status code:", response.status_code)
        return None

def get_pac_total_for_candidate(fec_id, cycle):
    try:
        api_response = get_candidate(fec_id, cycle)
    except:
        # Catching any unforseen errors
        api_response = None
    # print("api_response")
    print("Getting pac total for cand", fec_id, cycle)
    if api_response is not None:
        if api_response["status"] == "OK":
            results = api_response["results"]
            if len(results) > 0:
                candidate = results[0]
                amount = candidate["total_from_pacs"]
                return amount
            else:
                print("Got an empty results list")
                return 0.0 # Again somehow got no results
        else:
            print("Got bad status code:", api_response["status"])
            return 0.0 # Nobody found for this fec is
    else:
        print("Got an improper response from api")
        return 0.0


def fill_pac_totals(df, cycles):
    """
    Fills the given dataframe (containing members and their FEC ids) with pac totals for all cycles

    Args:
        df (DataFrame): A dataframe containing members of congress and their FEC ids
    """
    ret_df = df[["name", "fec_candidate_id"]]

    for c in cycles:
        print("Getting pac totals for cycle:", c)
        print(ret_df["fec_candidate_id"].head)
        ret_df[c] = df["fec_candidate_id"].apply(lambda x : get_pac_total_for_candidate(x, c))
        print(ret_df[c])
        ret_df.to_csv("temp-" + c + ".csv")
    
    return ret_df


def run():
    # Starting with all of the members we have downloaded
    all_members_df = pd.read_csv("members.csv")

    

    # Filtering such that it is just the ones that have FEC ids (weirdly 210-213 congresses largely do not)
    only_fec_id_members = all_members_df[all_members_df["fec_candidate_id"].notnull()]

    # Removing all duplicate members based on name (Hope this doesn't accidentally remove too many!)
    no_dup_members = only_fec_id_members.drop_duplicates(subset=["name"], keep="last")

    print(len(no_dup_members))

    # Resetting the index because it gets all funky
    members_and_ids = no_dup_members[["name", "party", "fec_candidate_id"]].reset_index(drop=True)


    # print(members_and_ids)

    cycles = ["2010", "2012", "2014", "2016", "2018", "2020"]

    final_df = fill_pac_totals(members_and_ids, cycles)

    print(final_df.head)

    final_df.to_csv("members_pac_totals.csv")
    
    



if __name__ == "__main__":
    run()
