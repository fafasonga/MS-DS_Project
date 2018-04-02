import os
from datetime import datetime

import pandas as pd
import pyproj

geod = pyproj.Geod(ellps='WGS84')

headers_trajectory = ['latitude', 'longitude', 'null', 'altitude', 'timestamp_float', 'date', 'time']


def load_trajectory_df(full_filename):
    subfolder = full_filename.split('/')[-3]

    df = pd.read_csv(full_filename, skiprows=6, header=None, names=headers_trajectory)

    df['date'] = df.apply(lambda z: datetime.strptime(z.date, "%Y-%m-%d").strftime("%d/%m/%Y"), axis=1)
    df['time'] = df.apply(lambda z: z.time, axis=1)
    df = df.drop(['null', 'timestamp_float', 'altitude'], axis=1)

    return df


LABELS_FILE = 'labels.txt'
MAIN_FOLDER = 'Data/'
TRAJ_FOLDER = 'Trajectory/'
OUTPUT_FOLDER = 'processed_data/'

if __name__ == '__main__':

    # dir_target = input("Please, give a path to data: ").strip()
    dir_target = "/Users/admin/Downloads/Geolife Trajectories 1.3"
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

        output_filename = OUTPUT_FOLDER + subfolder + '.csv'
        # if True:
        #     print(df_traj_all)
        #     sys.exit(0)
        # continue
        print("Saving as: {}".format(os.path.abspath(output_filename)))
        df_traj_all.to_csv(output_filename, index=False, columns=cols, sep=";")
        del df_traj_all
