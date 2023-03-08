import os
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import wikipedia
from urllib.parse import quote

# This file is used to get the pageviews for a list of events from Wikipedia as well as the links from each event page.

class RowObject:
    def __init__(self, name, event_date, category):
        self.name = name
        self.event_date = event_date
        self.category = category

# read csv file
csv_file = pd.read_csv('eventsList.csv')

rows_list = []
for index, row in csv_file.iterrows():
    name = row['Name']
    event_date = datetime.strptime(str(row['EventDate']), '%Y%m%d')
    category = row['Category']
    row_object = RowObject(name, event_date, category)
    rows_list.append(row_object)

# function to get all the appropriate dates
def get_date_range(event_date):
    start_date = event_date - timedelta(days=30)
    end_date = event_date + timedelta(days=30)
    date_range = []
    while start_date <= end_date:
        date_range.append(start_date.strftime('%Y%m%d'))
        start_date += timedelta(days=1)
    return date_range


# loop through each row
for row in rows_list:

    # specify the page title and the date range
    page_title = row.name
    #URI encode the page title
    #page_title = quote(page_title)
    
    date_range = get_date_range(row.event_date)

    try:

        folder_name = page_title

        filename = f"{page_title}.csv"
        sub_folder = page_title
        sub_folder_path = os.path.join(row.category, "Views", sub_folder)
        

        file_path = os.path.join(sub_folder_path, filename)

        if not os.path.exists(file_path):

            

            # set the headers for the request
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }

            # make the API requests with the headers
            data = []
            for date in date_range:
                url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/all-agents/{page_title}/daily/{date}/{date}"
                response = requests.get(url, headers=headers)
                json_data = json.loads(response.text)
                data += json_data['items']

            # extract the view count for each day and save as a CSV file
            rows = []
            for item in data:
                date = item["timestamp"][:8]  # extract the date part from the timestamp
                views = item["views"]
                rows.append({'Date': date, 'Views': views})

            if not os.path.exists(sub_folder_path):
                os.makedirs(sub_folder_path)
            
            
            df = pd.DataFrame(rows)
            df.to_csv(file_path, index=False)
            
            print(f"Created {file_path}")

            # Get links from Wikipedia and save to a text file
            def write_links_to_file(page_name):
                page = wikipedia.page(page_name, auto_suggest=False)
                links = page.links
                folder_name = row.category
                if not os.path.exists(folder_name):
                    os.mkdir(folder_name)

                file_path = os.path.join(folder_name, "Links", f"{page_name}.txt")
                with open(file_path, "w") as file:
                    #First line is the event date
                    file.write(str(row.event_date) + "\n")
                    for link in links:
                        file.write(link + "\n")
                print(f"All links from '{page_name}' have been saved to /{folder_name}/Links/{page_name}/{page_name}.txt.")
            write_links_to_file(row.name)
        else:
            print(f"File already exists: {file_path}")
    
    except:
        print(f"\033[91mCould not get data for {row.name}\033[0m")
        #Add the page title to a text file named "failedPages.txt"
        #if the page title is not already in the file
        if row.name not in open("failedPagesPrimary.txt").read():
            with open("failedPagesPrimary.txt", "a") as file:
                file.write(row.name + "\n")

