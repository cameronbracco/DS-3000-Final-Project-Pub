from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import random

import html_to_csv


def get_search_url(company_name):
    """Gets the search url on OpenSecrets for a given company name

    Args:
        company_name ([string]): Name of the company to use as a search term

    Returns:
        [string]: URL to be scraped on OpenSecrets for searching their organizations
    """
    return "https://www.opensecrets.org/search?q=" + company_name + "&type=orgs"

def get_company_id(company):
    """Gets the OpenSecrets ID for a given company by scraping the search page if it can be found

    Args:
        company ([string]): The company name to use as a search team

    Returns:
        [string or None]: The OpenSecrets ID, if it could be found, otherwise None
    """
    print("MAKING SEARCH FOR COMPANY ID....")
    search_url = get_search_url(company)
    company_search_page = requests.get(search_url)

    if company_search_page.status_code == 200:
        print("GOOD RESPONSE....")
        page_soup = BeautifulSoup(company_search_page.content, 'html.parser')

        possible_orgs = page_soup.find_all("tr", id="organization")
        print(possible_orgs)

        if len(possible_orgs) > 0:
            best_org = possible_orgs[0].find("a")

            org_id = best_org["href"]
            org_name = best_org.get_text()
            print("FOUND BEST ORG:", org_name, org_id)
            splits = org_id.split("id=")
            return splits[1] # Just the part of the id link that we actually want
        else:
            return None
    else:
        print("BAD RESPONSE", company_search_page.status_code)
        return None

def get_data_url(company_id, cycle):
    """Gets the data url on OpenSecrets for a given company name and for a particular cycle

    Args:
        company_id ([string]): OpenSecrets ID for a company
        cycle ([string]): Cycle year to get data for (ex: 2020, 2018, 2016)

    Returns:
        [string]: Url to be scraped on OpenSecrets for the data
    """
    return "https://www.opensecrets.org/orgs/chevron/recipients?toprecipscycle=" + cycle \
            + "&id=" + company_id + "&candscycle=" + cycle
    # https://www.opensecrets.org/orgs/chevron/recipients?toprecipscycle=2020&id={ID}&candscycle=2020

def get_data_table_string(company_id, cycle):
    """Gets the data table of contributions by scraping an organization's OpenSecrets page

    Args:
        company_id ([string]): OpenSecrets ID for a company
        cycle ([string]): Cycle year to get data for (ex: 2020, 2018, 2016)
    """
    print("SCRAPING FOR COMPANY DATA....")
    data_url = get_data_url(company_id, cycle)
    company_data_page = requests.get(data_url)

    if company_data_page.status_code == 200:
        print("GOOD RESPONSE...")
        page_soup = BeautifulSoup(company_data_page.content, 'html.parser')

        possible_tables = page_soup.find_all("table")
        for table in possible_tables:
            # print(table.attrs)
            if "data-collection" in table.attrs:
                table_str = table["data-collection"]
                if table["data-title"] == "":
                    print("Found the table!")
                    return table_str
        
        return None

    else:
        print("BAD RESPONSE:", company_data_page.status_code)
        return None

def run_companies(sector, companies, cycles):
    """
    Scrapes OpenSecrets for a specific set of companies for a specific set of cycles.
    This function saves raw data into csv files for each company, for each cycle, as
    well as returns a dataframe with all of the IDs matching the companies in case it is useful
    at a later point.

    Returns:
        A DataFrame containing the ids of the companies that it found
    """
    found_companies = []

    for company in companies:
        print("STEP 1: Get company ID for", company)
        company_id = get_company_id(company)

        if company_id is not None:
            print("Got", company, "id:", company_id)
            found_companies.append({"Company": company, "id": company_id})
            for cycle in cycles:
                print("STEP 2: Get the data table string for cycle", cycle)

                path = "data/" + sector + "/" + cycle + "/"
                data_str = get_data_table_string(company_id, cycle)
                if data_str is not None:
                    html_to_csv.export_json_to_csv(data_str, company, cycle, save_path=path)
                else:
                    print("Was not able to get the data for company", company, "for cycle", cycle)
                
                cycle_sleep_time = random.randrange(2,6)
                print("Sleeping (between cycles) for", cycle_sleep_time)
                time.sleep(cycle_sleep_time)
        else:
            print("Company id was None, what do")
        
        company_sleep_time = random.randrange(5, 10)
        print("Sleeping (between companies) for", company_sleep_time)
        time.sleep(company_sleep_time)
    
    return found_companies


def run_sectors(sectors, cycles):
    """
    Runs company contribution scraping for all of the sectorrs
    Currently available sectors are
        oil
        solar
        wind
        hydro
        nuclear
        coal
    """
    

    for sector in sectors:
        print("Beginning scraping of sector:", sector)
        companies_df = pd.read_csv("data/" + sector + "/" + sector + "-companies.csv")

        companies = companies_df["Company"]
        found_companies = run_companies(sector, companies, cycles)

        # Creating a new dataframe that comes with ids!
        new_companies_df = pd.DataFrame(found_companies)

        new_companies_df.to_csv("data/" + sector + "/" + sector + "-companies-ids.csv")


if __name__ == "__main__":
    print("Starting scraping program")
    SECTORS = ["solar"] #, "oil", "wind", "hydro", "nuclear", "coal"]
    CYCLES = ["2020", "2018", "2016", "2014", "2012", "2010", "2008"]
    run_sectors(SECTORS, CYCLES)





