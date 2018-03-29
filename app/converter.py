import datetime as dt
import os
from math import cos

import pandas as pd
import pyproj

geod = pyproj.Geod(ellps='WGS84')

headers_trajectory = ['X', 'Y', 'Timestamp']

def load_trajectory_df(full_filename):
    df = pd.read_csv(full_filename, header=None, names=headers_trajectory)

    lat = 46.716524
    lon = 11.652545

    for itm in range(len(df)):
        a = df['Y'][itm] / (6076 / 60)
        b = df['X'][itm] / (4145 / 60)
        c = lon + b[itm]
        latitude = lat + a[itm]
        df['latitude'] = df.apply(latitude)

        longitude = c - (df['X'][itm] / (6076 * cos(itm)) / 60)
        df['longitude'] = df.apply(longitude)
        df['date'] = df.apply(dt.datetime.datetime.fromtimestamp(int(df['Timestamp'][itm])).strftime('%d/%m/%Y'), axis=1)
        df['time'] = df.apply(dt.datetime.datetime.fromtimestamp(int(df['Timestamp'][itm])).strftime('%H:%M:%S'), axis=1)
        df['Timestamp'] = df.apply(
            dt.datetime.datetime.fromtimestamp(int(df['Timestamp'][itm])).strftime('%d/%m/%Y %H:%M:%S'), axis=1)

    return df


LABELS_FILE = 'labels.txt'
MAIN_FOLDER = 'Data'
TRAJ_FOLDER = 'Trajectory/'
OUTPUT_FOLDER = 'processed_data/'

if __name__ == '__main__':

    # dir_target = input("Please, give a path to data: ").strip()
    dir_target = "/Users/admin/Downloads/geo/"
    os.chdir(dir_target)

    for f in os.listdir(os.path.curdir):
        print(f)

    # sys.exit(0)

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    directories = os.listdir(MAIN_FOLDER)

    for subfolder in directories:
        list_df_traj = []
        subfolder_ = MAIN_FOLDER + subfolder + '/'
        traj_folder = MAIN_FOLDER + subfolder + '/' + TRAJ_FOLDER
        traj_files = os.listdir(traj_folder)

        traj_files_full_path = [traj_folder + traj_file for traj_file in traj_files]
        print(subfolder, len(traj_files_full_path))

        for file in traj_files_full_path:
            list_df_traj.append(load_trajectory_df(file))

        cols = ""
        for df in list_df_traj:
            df['name'] = OUTPUT_FOLDER + subfolder
            cols = df.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            df = df.ix[:, cols]

        # sys.exit(1)
        df_traj_all = pd.concat(list_df_traj)
        list_df_traj = []

        if LABELS_FILE in os.listdir(subfolder_):
            filename = subfolder_ + LABELS_FILE

        output_filename = subfolder + '.csv'
        # if True:
        #     print(df_traj_all)
        #     sys.exit(0)
        # continue
        print("Saving as: {}".format(os.path.abspath(output_filename)))
        df_traj_all.to_csv(output_filename, index=False, columns=cols, sep=";")
        del df_traj_all
