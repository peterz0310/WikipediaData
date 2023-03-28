import csv
import os
import sys
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


def main():
    # Get the directory to search for CSV files.
    root_dir = os.path.join(sys.argv[1], 'Graph Analysis')

        # Loop over the folders in the root directory.
    for folder_name in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder_name)

            # Check if the folder contains CSV files.
        if os.path.isdir(folder_path):
            csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

            if len(csv_files) > 0:
                # Create a list to hold the "percent" values and file names from each CSV file.
                x = []
                y = []        

                # Loop over the CSV files in the folder.
                for csv_file in csv_files:
                    
                    with open(os.path.join(folder_path, csv_file), 'r') as f:
                        csv_reader = csv.reader(f)
                        next(csv_reader) # skip header row
                        rows = list(csv_reader)
                        #x.append(row[0] for row in rows)
                        #y.append(int(row[1]) for row in rows) # select rows 3 to 57
                        x.append([os.path.splitext(csv_file)[0]])
                        y.append([os.path.splitext(csv_file)[1]])

                        #plt.plot([1, 2, 3, 4])
                        #plt.ylabel('some numbers')
                        #plt.show(block=False)      
                        #print(x)
                        
                        plt.plot([x],[y])
            
                        plt.xlabel('Topic')
                        plt.ylabel('Percent Increase')
                        plt.title('Trends in Views')
                        plt.show(block=False)
                        

if __name__ == '__main__':
    main()                     


