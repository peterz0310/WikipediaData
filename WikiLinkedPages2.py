import sys
import os
import json
import pandas as pd
from datetime import datetime, timedelta
import requests
from multiprocessing import Pool, cpu_count

category = sys.argv[1]
path = os.path.join(category, "Links")

def get_date_range(event_date_str):
    event_date = datetime.strptime(event_date_str.strip(), '%Y-%m-%d')
    start_date = event_date - timedelta(days=30)
    end_date = event_date + timedelta(days=30)
    date_range = []
    while start_date <= end_date:
        date_range.append(start_date.strftime('%Y%m%d'))
        start_date += timedelta(days=1)
    return date_range

def scrape_data(link):
    page_title = link.strip()
    file_name = f"{page_title}.csv"
    sub_folder = filename[:-4]
    sub_folder_path = os.path.join(category, "Views", sub_folder)
    file_path = os.path.join(sub_folder_path, file_name)
    if os.path.exists(file_path):
        print(f"{file_path} already exists.")
        return
    
    print("Trying", page_title, "...")
    date_range = get_date_range(event_date.strip().split()[0])
    # set the headers for the request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    data = []
    try:
        for date in date_range:
            url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/all-agents/{page_title}/daily/{date}/{date}"
            response = requests.get(url, headers=headers)
            json_data = json.loads(response.text)
            data += json_data['items']
    except:
        print("\033[91m" + "Error getting data on " + page_title+"." + '\033[0m')
        #Add page title to a txt file 
        if page_title not in open("failedPagesPrimary.txt").read():
            with open("failedPagesSecondary.txt", "a") as file:
                file.write(page_title+"\n")
        return

    # extract the view count for each day and save as a CSV file
    rows = []
    try:
        for item in data:
            date = item["timestamp"][:8]  # extract the date part from the timestamp
            views = item["views"]
            rows.append({'Date': date, 'Views': views})

        file_path = os.path.join(sub_folder_path, file_name)
        df = pd.DataFrame(rows)
        df.to_csv(file_path, index=False)

        print(f"Created {file_path}")
    except:
        print("\033[91m" + "Error creating " + file_path + "." + '\033[0m')
        return

for filename in os.listdir(path):
    if filename.endswith(".txt"):
        with open(os.path.join(path, filename), "r", encoding="utf-8") as file:
            links = file.readlines()
            event_date = links[0].strip()
            links = links[1:]
            links = [link.strip() for link in links]
            
            pool = Pool(cpu_count())
            pool.map(scrape_data, links)
            pool.close()
            pool.join()
