import os
import sys
import glob
import pandas as pd
import matplotlib.pyplot as plt

def plot_csv_files(root_dir):
    views_dir = os.path.join(root_dir, "Views")

    for folder in glob.glob(os.path.join(views_dir, '*')):
        if os.path.isdir(folder):
            plot_folder = os.path.join(views_dir, "Plots", os.path.basename(folder))
            if not os.path.exists(plot_folder):
                os.makedirs(plot_folder)
            for file in glob.glob(os.path.join(folder, '*.csv')):
                plot_csv_file(file, plot_folder)

def plot_csv_file(csv_file, plot_dir):
    df = pd.read_csv(csv_file)
    if "Date" in df.columns and "Views" in df.columns:
        plt.figure()
        dates = pd.to_datetime(df["Date"], format='%Y%m%d')
        plt.plot(dates, df["Views"])
        plt.xlabel("Date")
        plt.ylabel("Views")
        plt.title(os.path.splitext(os.path.basename(csv_file))[0])

        ax = plt.gca()
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

        plt.savefig(os.path.join(plot_dir, f"{os.path.splitext(os.path.basename(csv_file))[0]}.png"))
        plt.close()




if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python plot_csv_files.py <root_directory>")
        sys.exit(1)

    root_directory = sys.argv[1]
    plot_csv_files(root_directory)
