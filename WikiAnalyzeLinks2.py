import csv
import os
import sys
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

def main():
    # Get the directory to search for CSV files.
    root_dir = os.path.join(sys.argv[1], 'Views')

    # Loop over the folders in the root directory.
    for folder_name in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder_name)

        # Check if the folder contains CSV files.
        if os.path.isdir(folder_path):
            csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

            if len(csv_files) > 0:
                # Create a list to hold the "Views" values and file names from each CSV file.
                views_data = []
                percent_data = []
                x = []
                y = []

                # Loop over the CSV files in the folder.
                for csv_file in csv_files:
                    with open(os.path.join(folder_path, csv_file), 'r') as f:
                        csv_reader = csv.reader(f)
                        next(csv_reader) # skip header row
                        rows = list(csv_reader)
                        views = [int(row[1]) for row in rows[2:58]] # select rows 3 to 57
                        baseline_index = views.index(min(views))
                        baseline_value = round(sum(views[baseline_index-2:baseline_index+3])/5, 2)
                        baseline_date = datetime.strptime(rows[baseline_index+2][0], '%Y%m%d').strftime('%m/%d/%Y')
                        peak_index = views.index(max(views))
                        peak_value = round(sum(views[peak_index-2:peak_index+3])/5, 2)
                        peak_date = datetime.strptime(rows[peak_index+2][0], '%Y%m%d').strftime('%m/%d/%Y')
                        try:
                            percent_increase = round((peak_value - baseline_value) / baseline_value * 100, 2)
                        except ZeroDivisionError:
                            percent_increase = 0
                        views_data.append([os.path.splitext(csv_file)[0], baseline_value, baseline_date, peak_value, peak_date, percent_increase])
                        percent_data.append([os.path.splitext(csv_file)[0], percent_increase])
                        x.append(os.path.splitext(csv_file)[0])
                        y.append(int(percent_increase))
                        #x = np.array([x])
                        #y = np.array([y])

                plt.plot(x,y) #for all data points
                #plt.plot(x[1:5],y[1:5]) #for less data points and easier-to-read graph
                plt.xlabel('Topic')
                plt.ylabel('Percent Increase')
                plt.title('Trends in Views')
                plt.show()
            


                # Write the "Views" values and file names to a new CSV file.
            output_dir = os.path.join(sys.argv[1], 'Analysis')
            os.makedirs(output_dir, exist_ok=True)
            output_file_path = os.path.join(output_dir, f'{folder_name}.csv')
            with open(output_file_path, 'w', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(['File', 'Baseline', 'Baseline Date', 'Peak', 'Peak Date', 'Percent Increase'])
                csv_writer.writerows(views_data)
                
            output_dir1 = os.path.join(sys.argv[1], 'Graph Analysis')
            os.makedirs(output_dir1, exist_ok=True)
            output_file_path = os.path.join(output_dir1, f'{folder_name}.csv')
            with open(output_file_path, 'w', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(['File', 'Percent Increase'])
                csv_writer.writerows(percent_data)
                
    print('Analysis complete. Output saved in:', output_dir + " and " + output_dir1 + "/")

if __name__ == '__main__':
    main()
